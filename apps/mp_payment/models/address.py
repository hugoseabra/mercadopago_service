import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import EntityMixin, DomainRuleMixin


class Address(models.Model, EntityMixin, DomainRuleMixin):
    """
    Customer's address
    """

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        unique_together = (
            ('customer', 'slug',),
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
        related_name='addresses',
    )
    name = models.CharField(
        _('name'),
        max_length=32,
        help_text=_('A name to identify the address.'),
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=64,
        help_text=_('Unique identification of the address.'),
        null=False,
        blank=False,
    )
    street_name = models.CharField(
        _('street name'),
        max_length=255,
        null=False,
        blank=False,
    )
    street_number = models.CharField(
        _('street number'),
        max_length=32,
        null=True,
        blank=True,
    )
    neighborhood_id = models.CharField(
        _('neighborhood ID'),
        max_length=16,
        null=True,
        blank=True,
    )
    neighborhood_name = models.CharField(
        _('neighborhood name'),
        max_length=255,
        null=True,
        blank=True,
    )
    zip_code = models.CharField(
        _('zip code'),
        max_length=32,
        null=True,
        blank=True,
    )
    city_id = models.CharField(
        _('city ID'),
        max_length=16,
        null=True,
        blank=True,
    )
    city_name = models.CharField(
        _('city name'),
        max_length=255,
        null=True,
        blank=True,
    )
    state_id = models.CharField(
        _('state ID'),
        max_length=16,
        null=True,
        blank=True,
    )
    state_name = models.CharField(
        _('state name'),
        max_length=255,
        null=True,
        blank=True,
    )
    country_id = models.CharField(
        _('country ID'),
        max_length=16,
        null=True,
        blank=True,
    )
    country_name = models.CharField(
        _('country name'),
        max_length=255,
        null=True,
        blank=True,
    )
    phone_area_code = models.CharField(
        _('phone area code'),
        max_length=5,
        help_text=_('A phone number to contact anyone on this address.'),
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=32,
        help_text=_('A phone number to contact anyone on this address.'),
        null=True,
        blank=True,
    )
    comments = models.TextField(
        _('comments'),
        help_text=_('Any extra information about this address.'),
        null=True,
        blank=True,
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
        return '<Address {}: {}, owner: {}>'.format(self.pk,
                                                    self.name,
                                                    self.customer_id, )

    def __str__(self):
        return self.name
