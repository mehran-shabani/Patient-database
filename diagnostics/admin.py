from django.contrib import admin
from .models import Diagnosis


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'diagnosis_description', 'diagnosis_code', 'is_primary', 'diagnosed_by', 'diagnosis_date']
    list_filter = ['is_primary', 'diagnosis_date', 'diagnosed_by']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'diagnosis_description', 'diagnosis_code']
    date_hierarchy = 'diagnosis_date'
    ordering = ['-diagnosis_date']
