from django.contrib import admin
from .models import ClinicalNote


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'note_type', 'provider', 'timestamp', 'is_signed', 'amended']
    list_filter = ['note_type', 'is_signed', 'amended', 'timestamp', 'provider']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'note_text']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
