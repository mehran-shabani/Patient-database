from django.contrib import admin
from .models import Procedure, ConsentForm


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'procedure_name', 'procedure_date', 'primary_surgeon', 
                    'anesthesiologist', 'duration_minutes', 'is_emergency']
    list_filter = ['is_emergency', 'procedure_date', 'primary_surgeon']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'procedure_name', 'procedure_code']
    date_hierarchy = 'procedure_date'
    ordering = ['-procedure_date']


@admin.register(ConsentForm)
class ConsentFormAdmin(admin.ModelAdmin):
    list_display = ['patient', 'consent_type', 'consent_status', 'sign_timestamp', 'witnessed_by']
    list_filter = ['consent_status', 'consent_type', 'sign_timestamp']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'consent_type']
    date_hierarchy = 'sign_timestamp'
    ordering = ['-sign_timestamp']
