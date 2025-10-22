from django.contrib import admin
from .models import Patient, Insurance


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['national_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_type', 'registration_date']
    list_filter = ['gender', 'blood_type', 'registration_date']
    search_fields = ['national_id', 'first_name', 'last_name', 'primary_phone_number']
    date_hierarchy = 'registration_date'
    ordering = ['-registration_date']


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider_name', 'policy_number', 'insurance_type', 'expiry_date']
    list_filter = ['insurance_type', 'provider_name']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'policy_number']
    date_hierarchy = 'expiry_date'
