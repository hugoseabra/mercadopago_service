import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin
from apps.mp_payment.rules.common_rules import (
    OnlyActiveAccountAllowedForCreation,
)
from apps.mp_payment.rules.notification_rules import PreferenceSameAccount


class Notification(models.Model, EntityMixin, DomainRuleMixin):
    """
    A notification received from MercadoPago.
    """

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notification')
        unique_together = (
            ('topic', 'resource_id',),
        )

    rules = [
        OnlyActiveAccountAllowedForCreation,
        PreferenceSameAccount,
    ]

    TOPIC_ORDER = 'o'
    TOPIC_PAYMENT = 'p'

    STATUS_PENDING = 'unp'
    STATUS_PROCESSED = 'pro'
    STATUS_IGNORED = 'ign'

    STATUS_OK = 'ok'
    STATUS_404 = '404'
    STATUS_ERROR = 'err'

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    account = models.ForeignKey(
        to='mp_payment.Account',
        verbose_name=_('owner'),
        related_name='notifications',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    preference = models.ForeignKey(
        to='mp_payment.Preference',
        verbose_name=_('preference'),
        related_name='notifications',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _('status'),
        max_length=3,
        choices=(
            (STATUS_PENDING, _('Pending')),
            (STATUS_PROCESSED, _('Processed')),
            (STATUS_IGNORED, _('Ignored')),
            (STATUS_OK, _('Okay')),
            (STATUS_404, _('Error 404')),
            (STATUS_ERROR, _('Error')),
        ),
        default=STATUS_PENDING,
    )
    topic = models.CharField(
        max_length=1,
        choices=(
            (TOPIC_ORDER, 'Merchant Order',),
            (TOPIC_PAYMENT, 'Payment',),
        ),
    )
    resource_id = models.CharField(
        _('resource_id'),
        max_length=46,
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        null=False,
        blank=False,
        editable=False,
    )
    last_update = models.DateTimeField(
        _('last_update'),
        auto_now=True,
    )

    @property
    def processed(self):
        return self.status == Notification.STATUS_PROCESSED

    def __repr__(self):
        return '<Notification {}: {} {}, owner: {}>'.format(
            self.id,
            self.get_topic_display(),
            self.resource_id,
            self.account_id,
        )

    def __str__(self):
        return '{} {}'.format(self.get_topic_display(), self.resource_id)
