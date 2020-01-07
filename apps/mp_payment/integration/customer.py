from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from apps.mp_payment.models import Customer
from .exceptions import SynchronizationException
from .response_utils import process_response


def synchronize(instance: Customer):
    """
    Synchronization to mercado pago.
    """

    if instance.deleted is True:
        raise SynchronizationException(
            status=0,
            error='cannot synchronize',
            message=_('Customer is scheduled to be deleted and cannot'
                      ' be synchronized')
        )

    service = instance.account.service
    customer_data = instance.to_mp_representation()

    from pprint import pprint
    pprint(customer_data)

    if instance.synchronized is False:
        uri = '/v1/customers'
        response = service.post(uri=uri, data=customer_data)
    else:
        del customer_data['email']
        uri = '/v1/customers/{id}'.format(id=instance.mp_id)
        response = service.put(uri=uri, data=customer_data)

    status, data = process_response(response)

    if 'id' not in data:
        search_response = service.get(
            uri='/v1/customers/search',
            params={'metadata.external_id': str(instance.pk)}
        )
        collection, status = process_response(search_response)

        if status == '200' and collection:
            mp_item = collection['results'][0]
            data['id'] = mp_item.get('id')

    if 'id' in data:
        instance.mp_id = data['id']
        instance.save()

    if 'default_card' in data and data['default_card']:
        try:
            card = instance.cards.get(mp_id=data['default_card'])
            instance.default_card_pk = card.pk
            instance.save()
        except ObjectDoesNotExist:
            pass

    elif instance.cards.count():
        card = instance.cards.first()
        if card.synchronized:
            instance.default_card_pk = card.pk
            instance.save()


def remove(instance: Customer):
    """
    Deletes at mercado pago.
    """

    if instance.deleted is False:
        raise SynchronizationException(
            status=0,
            error='cannot delete',
            message=_('Customer is not scheduled to be deleted and cannot'
                      ' be processed for deletion at mercado pago.')
        )

    if instance.synchronized is False:
        raise SynchronizationException(
            status=0,
            error='cannot delete',
            message=_('Customer has not been synchronized to be deleted.')
        )

    service = instance.account.service

    print('mercado pago id:', instance.mp_id)
    response = service.delete(
        uri='/v1/customers/{id}'.format(id=instance.mp_id)
    )

    status, data = process_response(response)
    print(status)
    print(data)
