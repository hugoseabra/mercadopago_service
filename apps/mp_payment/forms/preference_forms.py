from django import forms

from apps.mp_payment.models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = '__all__'
