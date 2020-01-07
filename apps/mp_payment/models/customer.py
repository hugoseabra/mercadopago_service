import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin


class Customer(models.Model, EntityMixin, DomainRuleMixin):
    """
    Customer identified as payer at Mercado Pago.
    """

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        unique_together = (
            ('account', 'external_id',),
        )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    account = models.ForeignKey(
        'mp_payment.Account',
        verbose_name=_('account'),
        related_name='customers',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    external_id = models.CharField(
        _('external ID'),
        max_length=255,
        help_text=_("External ID controlled by this application consumer."),
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=32,
        help_text=_("Customer's first name as to be registered as payer."),
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=32,
        help_text=_("Customer's last name as to be registered as payer."),
        null=False,
        blank=False,
    )
    is_company = models.CharField(
        _('last name'),
        max_length=32,
        help_text=_("Customer's last name as to be registered as payer."),
        null=False,
        blank=False,
    )
    email = models.EmailField(
        'E-mail',
        max_length=253,
        null=False,
        blank=False,
    )
    phone_area_code = models.CharField(
        _('phone area code'),
        max_length=5,
        null=False,
        blank=False,
    )
    phone_number = models.CharField(
        _('phone area code'),
        max_length=32,
        null=False,
        blank=False,
    )
    doc_type = models.CharField(
        _('doc. type'),
        max_length=32,
        null=False,
        blank=False,
    )
    doc_number = models.CharField(
        _('doc. number'),
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField(
        _('description'),
    )
    default_card_pk = models.UUIDField(
        _('default card'),
        null=True,
        blank=True,
    )
    test_customer = models.BooleanField(
        _('test customer'),
        help_text=_('Indicates that this customer is not a real customer.'),
        default=True,
        null=False,
        blank=True,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Indicates that the Customer can be used to process payments.'
        ),
    )
    deleted = models.BooleanField(
        _('deleted'),
        default=False,
        help_text=_(
            'Indicates that the Customer is deleted but has not been'
            ' synchronized to be deleted in mercado pago.'
        ),
    )
    mp_id = models.CharField(
        _('mercadopago ID'),
        max_length=32,
        help_text=_('The CUSTOMER_ID given by MercadoPago.'),
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
    def synchronized(self):
        return not (not self.mp_id)

    def __repr__(self):
        return '<Customer {}: {} {}>'.format(self.pk,
                                             self.first_name,
                                             self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def to_mp_representation(self):
        rep = {
            "id": self.mp_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": {
                "area_code": self.phone_area_code,
                "number": self.phone_number,
            },
            "identification": {
                "type": self.doc_type,
                "number": self.doc_number,
            },
            "description": self.description,
            "address":
                self.address.to_mp_representation() if self.address else None,
            "cards": [
                c.to_mp_representation()
                for c in self.cards.filter(active=True)
            ],
            "default_address": None,
            "default_card": None,
            "metadata": {
                'external_id': str(self.pk),
            }
        }
        if self.default_card_pk:
            try:
                card = self.cards.get(pk=self.default_card_pk)
                rep.update({'default_card': card.to_mp_representation()})
            except ObjectDoesNotExist:
                pass

        # address = None
        # if address_pk:
        #     try:
        #         address = self.addresses.get(pk=address_pk)
        #     except ObjectDoesNotExist:
        #         pass
        #
        # if not address and self.default_address_id:
        #     try:
        #         address = self.addresses.get(pk=self.default_address_id)
        #     except ObjectDoesNotExist:
        #         pass
        #
        # if address:
        #     rep.update({'address': address.to_mp_representation()})
        #
        # card = None
        # if card_pk:
        #     try:
        #         card = self.cards.get(pk=card_pk)
        #     except ObjectDoesNotExist:
        #         pass
        #
        # if not card and self.default_card_id:
        #     try:
        #         card = self.cards.get(pk=self.default_address_id)
        #     except ObjectDoesNotExist:
        #         pass
        #
        # if card:
        #     rep.update({'card': card.to_mp_representation()})

        return rep
