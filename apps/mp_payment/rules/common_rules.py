from apps.core.models.domain_ruler_mixin import RuleChecker, RuleIntegrityError


class OnlyActiveAccountAllowedForCreation(RuleChecker):
    """
    Rule: only active account can be used for new records.
    """

    def check(self, instance, *args, **kwargs):
        is_new = instance.is_new is True
        if is_new is True and instance.account.active is False:
            raise RuleIntegrityError(_('Inactive account cannot be used.'))


class OnlyActiveCustomerAllowedForCreation(RuleChecker):
    """
    Rule: only active customer can be used for new records.
    """

    def check(self, instance, *args, **kwargs):
        is_new = instance.is_new is True
        if is_new is True and instance.customer.active is False:
            raise RuleIntegrityError(_('Inactive customer cannot be used.'))
