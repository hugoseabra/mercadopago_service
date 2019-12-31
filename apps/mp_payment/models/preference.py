import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin
from apps.mp_payment.rules.common_rules import (
    OnlyActiveAccountAllowedForCreation,
)


class Preference(models.Model, EntityMixin, DomainRuleMixin):
    """
    An MP payment preference.

    Related data is send to MP and not stored locally - it's assumed
    it's part of the model that relates to this one.
    """
    class Meta:
        verbose_name = _('preference')
        verbose_name_plural = _('preferences')

    rules = [
        OnlyActiveAccountAllowedForCreation,
    ]

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    account = models.ForeignKey(
        'mp_payment.Account',
        verbose_name=_('owner'),
        related_name='preferences',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    title = models.CharField(
        _('title'),
        max_length=256,
    )
    price = models.DecimalField(
        _('price'),
        max_digits=15,
        decimal_places=2,
        null=False,
        blank=False,
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
        null=False,
        blank=True,
    )
    payment_url = models.URLField(
        _('payment url'),
    )
    sandbox_url = models.URLField(
        _('sandbox url'),
    )
    reference = models.CharField(
        _('reference'),
        max_length=128,
        unique=True,
    )
    paid = models.BooleanField(
        _('paid'),
        default=False,
        help_text=_('Indicates if the preference has been paid.'),
    )
    # Doc says it's a UUID. It's not.
    mp_id = models.CharField(
        _('mercadopago id'),
        max_length=46,
        help_text=_('The id MercadoPago has assigned for this Preference')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        null=False,
        blank=False,
        editable=False,
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        null=False,
        blank=False,
        editable=False,
    )

    @property
    def url(self):
        if self.account.sandbox:
            return self.sandbox_url
        else:
            return self.payment_url

    def __repr__(self):
        return '<Preference {}: mp_id: {}, paid: {}>'.format(
            self.id,
            self.mp_id,
            self.paid
        )

    def __str__(self):
        return self.mp_id
