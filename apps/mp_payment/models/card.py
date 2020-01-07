import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin


class Card(models.Model, EntityMixin, DomainRuleMixin):
    """
    Customer's card
    """

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')
        unique_together = (
            ('customer', 'first_six_digits', 'last_four_digits'),
        )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    customer = models.ForeignKey(
        to='mp_payment.Customer',
        verbose_name=_('owner'),
        help_text=_('customer who owns this address'),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='cards',
    )
    token = models.CharField(
        _('token'),
        max_length=32,
        null=True,
        blank=True,
        help_text=_("Required in credit card transactions."),
    )
    tmp_token = models.CharField(
        _('token'),
        max_length=32,
        null=True,
        blank=True,
        help_text=_("Required in credit card transactions."),
    )
    expiration_month = models.PositiveIntegerField(
        _('expiration month'),
        null=False,
        blank=False,
    )
    expiration_year = models.PositiveIntegerField(
        _('expiration year'),
        null=False,
        blank=False,
    )
    first_six_digits = models.CharField(
        _('first six digits'),
        max_length=6,
        null=False,
        blank=False,
    )
    last_four_digits = models.CharField(
        _('last four digits'),
        max_length=4,
        null=False,
        blank=False,
    )
    holder = models.CharField(
        _('holder'),
        max_length=32,
        help_text=_("Type the exact name pressed in the card."),
        null=False,
        blank=False,
    )
    comments = models.TextField(
        _('comments'),
        help_text=_('Any extra information about this address.'),
        null=True,
        blank=True,
    )
    deleted = models.BooleanField(
        _('deleted'),
        default=False,
        help_text=_(
            'Indicates that the card is deleted but has not been'
            ' synchronized to be deleted in mercado pago.'
        ),
    )
    mp_id = models.CharField(
        _('mercadopago ID'),
        max_length=16,
        help_text=_('The CARD_ID given by MercadoPago.'),
        unique=True,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Indicates that the Card can be used to process process payments.'
        ),
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
    def synchronized(self):
        return not (not self.mp_id)

    def __repr__(self):
        return '<Card {}: {}, customer: {}>'.format(self.pk,
                                                    self.holder,
                                                    self.customer_id, )

    def __str__(self):
        return self.holder

    def to_mp_representation(self):
        return {
            'customer_id': self.customer.mp_id,
            'expiration_month': self.expiration_month,
            'expiration_year': self.expiration_year,
            'cardholder': {
                'name': self.holder,
                'identification': {
                    'type': self.customer.doc_type,
                    'number': self.customer.doc_number,
                }
            },
        }
