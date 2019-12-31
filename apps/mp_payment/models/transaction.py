import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin
from apps.mp_payment.rules.common_rules import (
    OnlyActiveCustomerAllowedForCreation,
)
from apps.mp_payment.rules.transaction_rules import (
    AddressSameCustomer,
    CardSameCustomer,
    NotificationSamePreferenceAccount,
)


class Transaction(models.Model, EntityMixin, DomainRuleMixin):
    """
    Transações realizadas por cliente.
    """

    class Meta:
        verbose_name = _('customer transaction')
        verbose_name_plural = _('customer transactions')

    rules = [
        OnlyActiveCustomerAllowedForCreation,
        AddressSameCustomer,
        CardSameCustomer,
        NotificationSamePreferenceAccount,
    ]

    # The user has not yet completed the payment process.
    STATUS_PENDING = 'pending'

    # The payment has been approved and accredited.
    STATUS_APPROVED = 'approved'

    # The payment has been authorized but not captured yet.
    STATUS_AUTHORIZED = 'authorized'

    # Payment is being reviewed.
    STATUS_IN_PROCESSED = 'in_processed'

    # Users have initiated a dispute.
    STATUS_IN_MEDIATION = 'in_mediation'

    # Payment was rejected. The user may retry payment.
    STATUS_REJECTED = 'rejected'

    # Payment was cancelled by one of the parties or because time for payment
    # has expired
    STATUS_CANCELLED = 'cancelled'

    # Payment was refunded to the user.
    STATUS_REFUNDED = 'refunded'

    # Was made a chargeback in the buyer’s credit card.
    STATUS_CHARGED_BACK = 'charged_back'

    TYPE_BOLETO_BRADESCO = 'bolbradesco'
    TYPE_CREDIT_CARD = 'credit_card'

    STATUSES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_AUTHORIZED, 'Authorized'),
        (STATUS_IN_PROCESSED, 'Processed'),
        (STATUS_IN_MEDIATION, 'Mediation'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELLED, 'Cancalled'),
        (STATUS_REFUNDED, 'Refunded'),
        (STATUS_CHARGED_BACK, 'Chargedback'),
    )

    TRANSACTION_TYPES = (
        (TYPE_BOLETO_BRADESCO, _('Boleto bradesco')),
        (TYPE_CREDIT_CARD, _('Credit card')),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    preference = models.ForeignKey(
        to='mp_payment.Preference',
        verbose_name=_('preference'),
        related_name='transactions',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    customer = models.ForeignKey(
        to='mp_payment.Customer',
        verbose_name=_('customer'),
        help_text=_('Payer of the transaction.'),
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    address = models.ForeignKey(
        to='mp_payment.Address',
        verbose_name=_('address'),
        help_text=_('address used for payment.'),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    card = models.ForeignKey(
        to='mp_payment.Card',
        verbose_name=_('card'),
        help_text=_('card used for payment.'),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    notification = models.OneToOneField(
        to='mp_payment.Notification',
        verbose_name=_('notification'),
        related_name='customer_transaction',
        help_text=_('The notification that informed us of this payment.'),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _('status'),
        max_length=16,
        null=False,
        blank=False,
        choices=STATUSES,
    )
    status_detail = models.CharField(
        _('status detail'),
        max_length=32,
    )
    external_reference = models.CharField(
        _('external reference'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("External reference controlled by this application"
                    " consumer."),
    )
    token = models.CharField(
        _('token'),
        max_length=32,
        null=True,
        blank=True,
        help_text=_("Required in credit card transactions."),
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=False,
    )
    transaction_type = models.CharField(
        _('transaction type'),
        max_length=255,
        null=False,
        blank=False,
        choices=TRANSACTION_TYPES
    )
    transaction_amount = models.DecimalField(
        _('transaction amount'),
        decimal_places=10,
        max_digits=25,
        null=False,
        blank=False,
        help_text=_('Amount processed in provider with all taxes added.'),
    )
    original_amount = models.DecimalField(
        _('original amount'),
        decimal_places=10,
        max_digits=25,
        null=False,
        blank=False,
        help_text=_('Amount processed despite interests amount.'),
    )
    liquid_amount = models.DecimalField(
        _('liquid amount'),
        decimal_places=10,
        max_digits=25,
        null=True,
        blank=True,
        help_text=_('Amount to earn with taxes free.'),
    )
    taxes_amount = models.DecimalField(
        _('tax amount'),
        decimal_places=10,
        max_digits=25,
        null=True,
        blank=True,
        help_text=_('Taxes amount billed by consumer as profit.'),
    )
    provider_amount = models.DecimalField(
        _('provider amount'),
        decimal_places=10,
        max_digits=25,
        null=True,
        blank=True,
        help_text=_('Taxes amount billed by mercado pago.'),
    )
    interests_amount = models.DecimalField(
        _('interests amount'),
        decimal_places=10,
        max_digits=25,
        null=True,
        blank=True,
        help_text=_('When payment using credit card is paid with installment'
                    ' and interests incremented to the main amount.'),
    )
    statement_descriptor = models.CharField(
        _('statement descriptor'),
        max_length=11,
        null=False,
        blank=False,
        help_text=_('How it will appear in credit card report to customer.'),
    )
    installments = models.PositiveIntegerField(
        _('installments'),
        default=1,
        null=False,
        blank=True,
    )
    notification_url = models.TextField(
        _('notification'),
        null=False,
        blank=False,
        help_text=_('URL where Mercado Pago will send notifications about'
                    ' changes in transaction status.'),
    )
    boleto_url = models.TextField(
        verbose_name=_('URL do boleto'),
        null=True,
        blank=True,
    )
    boleto_expiration_date = models.DateField(
        _('vencimento do boleto'),
        null=True,
        blank=True,
    )
    boleto_barcode = models.DateField(
        _('vencimento do boleto'),
        null=True,
        blank=True,
    )
    mp_id = models.CharField(
        _('mercadopago ID'),
        max_length=16,
        help_text=_('The PAYMENT_ID given by MercadoPago.'),
    )
    created = models.DateTimeField(
        _('created'),
        editable=False,
    )
    approved = models.DateTimeField(
        _('approved'),
        null=True,
        editable=False,
    )

    @property
    def paid(self):
        return self.status == self.STATUS_APPROVED

    @property
    def pending(self):
        return \
            self.status == self.STATUS_IN_PROCESSED \
            or self.status == self.STATUS_AUTHORIZED

    @property
    def cancelled(self):
        return \
            self.status == self.STATUS_REFUNDED \
            or self.status == self.STATUS_REFUNDED \
            or self.status == self.STATUS_CHARGED_BACK

    def __repr__(self):
        return '<CustomerTransaction {}: {} {} - {}, customer: {}>'.format(
            self.id,
            self.get_transaction_type_display(),
            self.get_status_display(),
            round(self.transaction_amount, 2),
            self.customer_id,
        )

    def __str__(self):
        return '{} {}'.format(
            self.get_transaction_type_display(),
            round(self.transaction_amount, 2)
        )
