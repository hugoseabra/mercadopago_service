from django import forms

from apps.mp_payment.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.is_new = True
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()



        return cleaned_data
