import logging
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin
from apps.mp_payment.rules.common_rules import (
    OnlyActiveAccountAllowedForCreation,
)

logger = logging.getLogger(__name__)


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
        verbose_name=_('account'),
        related_name='preferences',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    title = models.CharField(
        _('title'),
        max_length=256,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )
    currency = models.CharField(
        _('currency'),
        max_length=5,
        default='BRL',
        null=False,
        blank=True,
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
        null=True,
        blank=True,
    )
    sandbox_url = models.URLField(
        _('sandbox url'),
        null=True,
        blank=True,
    )
    notification_url = models.URLField(
        _('notification url'),
        null=True,
        blank=True,
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
    deleted = models.BooleanField(
        _('deleted'),
        default=False,
        help_text=_(
            'Indicates that the Preference is deleted but has not been'
            ' synchronized to be deleted in mercado pago.'
        ),
    )
    # Doc says it's a UUID. It's not.
    mp_id = models.CharField(
        _('mercadopago id'),
        max_length=46,
        help_text=_('The id MercadoPago has assigned for this Preference'),
        null=True,
        blank=True,
        unique=True,
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

    @property
    def synchronized(self):
        return not (not self.mp_id)

    # def poll_status(self):
    #     """
    #     Manually poll for the status of this preference.
    #     """
    #     service = self.account.service
    #     payments = service.search_payment({
    #         'external_reference': self.reference,
    #     })
    #
    #     if not payments:
    #         logger.info('Polled for {}}. No data'.format(self.pk))
    #
    #
    #     logger.info('Polled for {}. Creating Payment'.format(self.pk))
    #
    #     return Payment.objects.create_or_update_from_raw_data(
    #         response['results'][-1]
    #     )
    #
    #     if response['results']:
    #     else:

    def __repr__(self):
        return '<Preference {}: mp_id: {}, paid: {}>'.format(
            self.id,
            self.mp_id,
            self.paid
        )

    def __str__(self):
        return self.mp_id

    def to_mp_representation(self):
        rep = {
            'id': self.mp_id,
            'payment_url': self.payment_url,
            'sandbox_url': self.sandbox_url,
            'notification_url': self.notification_url,
            'auto_return': 'all',
            'items': [
                {
                    'title': self.title,
                    'currency_id': self.currency,
                    'description': self.description,
                    'category_id': 'services',
                    'quantity': self.quantity,
                    # In case we get something like Decimal:
                    'unit_price': round(self.price, 2),
                }
            ],
            'external_reference': self.reference,
            'back_urls': {
                'success': None,
                'pending': None,
                'failure': None,
            },
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return rep
