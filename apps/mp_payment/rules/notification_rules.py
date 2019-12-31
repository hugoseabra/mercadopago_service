from apps.core.models.domain_ruler_mixin import RuleChecker, RuleIntegrityError


class PreferenceSameAccount(RuleChecker):
    """
    Rule: preference must be related to the same account as preference
    directly related.
    """

    def check(self, instance, *args, **kwargs):
        if not instance.preference_id:
            return

        if instance.preference.account_id != instance.account_id:
            raise RuleIntegrityError(
                _('Preference cannot be used for it is not related to same'
                  ' account of the notification.')
            )
