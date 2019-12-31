from django import forms

from apps.mp_payment.models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
