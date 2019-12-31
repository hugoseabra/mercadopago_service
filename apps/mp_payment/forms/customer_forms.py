from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.mp_payment.models import Customer, Address, Card


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
