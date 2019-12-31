from django import forms

from apps.mp_payment.models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
