import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin


class Account(models.Model, EntityMixin, DomainRuleMixin):
    """
    A mercadopago account, aka "application".
    """

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    name = models.CharField(
        _('name'),
        max_length=32,
        help_text=_('A friendly name to recognize this account.'),
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=64,
        unique=True,
        help_text=_("This slug is used for this account's notification URL."),
        null=False,
        blank=False,
    )
    app_id = models.CharField(
        _('client id'),
        max_length=16,
        help_text=_('The APP_ID given by MercadoPago.'),
        editable=False,
    )
    secret_key = models.CharField(
        _('secret key'),
        max_length=32,
        help_text=_('The SECRET_KEY given by MercadoPago.'),
        null=False,
        blank=False,
    )
    sandbox = models.BooleanField(
        _('sandbox'),
        default=True,
        help_text=_(
            'Indicates if this account uses the sandbox mode, '
            'indicated for testing rather than real transactions.'
        ),
    )
    active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Indicates that Account can be used to process process payments.'
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

    def __repr__(self):
        return '<Account {}: {}>'.format(self.pk, self.name)

    def __str__(self):
        return self.name
