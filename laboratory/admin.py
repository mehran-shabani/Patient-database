from django.contrib import admin
from .models import LabResult, MicrobiologyResult


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'test_name', 'result_value', 'units', 'status', 
                    'is_abnormal', 'result_date', 'performed_by']
    list_filter = ['status', 'is_abnormal', 'result_date', 'test_name']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'test_name']
    date_hierarchy = 'result_date'
    ordering = ['-result_date']


@admin.register(MicrobiologyResult)
class MicrobiologyResultAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'specimen_type', 'organism_name', 'collection_date', 
                    'report_date', 'microbiologist']
    list_filter = ['specimen_type', 'collection_date', 'report_date']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'specimen_type', 'organism_name']
    date_hierarchy = 'report_date'
    ordering = ['-report_date']
