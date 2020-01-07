import json
import os
import tempfile

from django.db.transaction import atomic
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.mp_payment.models import Card
from project import settings


def get_card_number_file_path(tmp_token):
    base_tmp_dir = tempfile.gettempdir()
    # base_tmp_dir = settings.BASE_DIR

    cards_base_dir = os.path.join(base_tmp_dir, 'card_numbers')

    if os.path.isdir(cards_base_dir) is False:
        os.mkdir(cards_base_dir)

    return os.path.join(cards_base_dir, tmp_token + '.json')


def get_card_number(card: Card):
    file_path = get_card_number_file_path(card.tmp_token)

    if os.path.isfile(file_path) is True:
        try:
            data = json.load(open(file_path))
            return data['number'], data['cvv']
        except:
            pass

    return None


def delete_card_number_file(card: Card):
    file_path = get_card_number_file_path(card.tmp_token)

    if os.path.isfile(file_path) is True:
        os.remove(file_path)


class CreditCardWebTokenCaptureView(TemplateView):
    template_name = 'mp_payment/token_capture.html'

    def get_card(self, tmp_token: str):
        try:
            return Card.objects.get(tmp_token=tmp_token)
        except Card.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        customer = None
        card_number = None
        cvv = None

        card = self.get_card(self.request.GET.get('code'))
        if card:
            customer = card.customer
            card_number, cvv = get_card_number(card)

        ctx['card'] = card
        ctx['customer'] = customer
        ctx['next'] = self.request.GET.get('next')
        ctx['mp_public_key'] = settings.MP_PUBLIC_KEY
        ctx['card_number'] = card_number
        ctx['cvv'] = cvv

        return ctx

    def post(self, request, *args, **kwargs):

        data = request.POST
        token = data.get('token')
        next_url = data.get('next')

        if not token or not next_url:
            return self.get(request, *args, **kwargs)

        card = self.get_card(self.request.GET.get('code'))
        if not card:
            return self.get(request, *args, **kwargs)

        delete_card_number_file(card)

        card.token = token
        card.tmp_token = None
        card.save()


        return redirect(next_url)
