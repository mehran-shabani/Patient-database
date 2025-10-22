from django.contrib import admin
from .models import Vital, FlowsheetData


@admin.register(Vital)
class VitalAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'timestamp', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                    'heart_rate', 'temperature', 'oxygen_saturation', 'recorded_by']
    list_filter = ['timestamp', 'recorded_by']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 'encounter__patient__last_name']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']


@admin.register(FlowsheetData)
class FlowsheetDataAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'flowsheet_item_name', 'item_value', 'units', 'timestamp', 'recorded_by']
    list_filter = ['flowsheet_item_name', 'timestamp', 'recorded_by']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'flowsheet_item_name']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
