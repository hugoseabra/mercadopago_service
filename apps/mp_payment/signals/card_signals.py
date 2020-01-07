from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.mp_payment.models import Card


@receiver(pre_delete, sender=Card)
def remove_default_customer_card(instance: Card, **_):
    customer = instance.customer
    if customer.default_card_pk == instance.pk:
        customer.default_card_pk = None
        customer.save()
