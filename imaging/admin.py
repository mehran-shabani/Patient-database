from django.contrib import admin
from .models import ImagingResult


@admin.register(ImagingResult)
class ImagingResultAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'modality', 'body_part', 'imaging_date', 'radiologist', 'report_timestamp']
    list_filter = ['modality', 'imaging_date', 'body_part', 'radiologist']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'body_part', 'impressions']
    date_hierarchy = 'imaging_date'
    ordering = ['-imaging_date']
