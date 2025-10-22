from django.contrib import admin
from .models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['license_number', 'first_name', 'last_name', 'provider_type', 'specialty', 'is_active', 'date_joined']
    list_filter = ['provider_type', 'is_active', 'date_joined']
    search_fields = ['first_name', 'last_name', 'license_number', 'specialty']
    date_hierarchy = 'date_joined'
    ordering = ['last_name', 'first_name']
