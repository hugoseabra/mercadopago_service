from django import forms

from apps.mp_payment.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
