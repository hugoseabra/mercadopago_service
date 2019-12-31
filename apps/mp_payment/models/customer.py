import uuid

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

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
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
    # @TODO - Suporte a inserção de metadatas como tags
    default_address_id = models.UUIDField(
        _('default address'),
    )
    default_card_id = models.UUIDField(
        _('default card'),
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
            'Indicates that Customer can be used to process process payments.'
        ),
    )
    mp_id = models.CharField(
        _('mercadopago ID'),
        max_length=16,
        help_text=_('The CUSTOMER_ID given by MercadoPago.'),
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

    def __repr__(self):
        return '<Customer {}: {} {}>'.format(self.pk,
                                             self.first_name,
                                             self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
