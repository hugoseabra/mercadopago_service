from apps.core.models.domain_ruler_mixin import RuleChecker, RuleIntegrityError


class AddressSameCustomer(RuleChecker):
    """
    Rule: address must be related to the same customer as customer directly
    related.
    """

    def check(self, instance, *args, **kwargs):
        if not instance.address_id:
            return

        if instance.customer_id != instance.address.customer_id:
            raise RuleIntegrityError(
                _('Address cannot be used for it is not related to same'
                  ' customer of the transaction.')
            )


class CardSameCustomer(RuleChecker):
    """
    Rule: card must be related to the same customer as customer directly
    related.
    """

    def check(self, instance, *args, **kwargs):
        if not instance.card_id:
            return

        if instance.customer_id != instance.card.customer_id:
            raise RuleIntegrityError(
                _('Card cannot be used for it is not related to same'
                  ' customer of the transaction.')
            )


class NotificationSamePreferenceAccount(RuleChecker):
    """
    Rule: notification must be related to a preference of the same account.
    """

    def check(self, instance, *args, **kwargs):
        if not instance.notification_id:
            return

        if instance.notification.account_id != instance.preference.account_id:
            raise RuleIntegrityError(
                _('Card cannot be used for it is not related to same'
                  ' customer of the transaction.')
            )
