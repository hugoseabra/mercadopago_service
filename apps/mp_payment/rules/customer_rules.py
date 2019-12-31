from apps.core.models.domain_ruler_mixin import RuleChecker, RuleIntegrityError
from apps.mp_payment.models import Address, Card


class ValidDefaultAddressID(RuleChecker):
    """
    Rule: default address must be valid.
    """

    def check(self, instance, *args, **kwargs):
        address_id = instance.default_address_id
        if not address_id:
            return

        exists = Address.objects.filter(
            pk=address_id,
            customer_id=instance.pk,
        ).exists() is True

        if exists is False:
            raise RuleIntegrityError(_('Default address is invalid.'))


class ValidDefaultCardID(RuleChecker):
    """
    Rule: default card must be valid.
    """

    def check(self, instance, *args, **kwargs):
        card_id = instance.default_card_id
        if not card_id:
            return

        exists = Card.objects.filter(
            pk=card_id,
            customer_id=instance.pk,
        ).exists() is True

        if exists is False:
            raise RuleIntegrityError(_('Default card is invalid.'))
