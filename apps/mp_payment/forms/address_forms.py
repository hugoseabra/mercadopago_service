from django import forms

from apps.mp_payment.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
