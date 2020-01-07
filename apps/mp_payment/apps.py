from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MpPaymentConfig(AppConfig):
    name = 'apps.mp_payment'
    label = 'mp_payment'
    verbose_name = _('Mercadopago Payments')

    # noinspection PyUnresolvedReferences
    def ready(self):
        import apps.mp_payment.signals
