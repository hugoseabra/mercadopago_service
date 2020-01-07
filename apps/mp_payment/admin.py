from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from . import models, forms


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    form = forms.AccountForm
    list_display = (
        'name',
        'slug',
        'app_id',
        'created_at',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    readonly_fields = (
        'access_token',
    )

    def access_token(self, obj):
        if obj.app_id and obj.secret_key:
            try:
                return obj.service.get_access_token()
            except Exception as e:
                pass

        return '-'

    access_token.short_description = _('access token')


@admin.register(models.Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'mp_id',
        'reference',
        'paid',
    )

    def poll_status(self, request, queryset):
        messages.add_message(
            request,
            messages.SUCCESS,
            'bla'
        )

    poll_status.short_description = _('poll status')

    actions = (
        poll_status,
    )
