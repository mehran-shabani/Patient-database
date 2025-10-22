from django.contrib import admin
from .models import Medication, MedicationAdministration


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'medication_name', 'dosage', 'frequency', 'duration_days', 
                    'provider', 'prescribed_date', 'is_active']
    list_filter = ['is_active', 'prescribed_date', 'provider']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'medication_name']
    date_hierarchy = 'prescribed_date'
    ordering = ['-prescribed_date']


@admin.register(MedicationAdministration)
class MedicationAdministrationAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'medication_name', 'dosage_given', 'route', 'administration_time', 
                    'administered_by', 'patient_refusal']
    list_filter = ['route', 'patient_refusal', 'administration_time', 'administered_by']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'medication_name']
    date_hierarchy = 'administration_time'
    ordering = ['-administration_time']
