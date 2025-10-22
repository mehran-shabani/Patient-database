from django.contrib import admin
from .models import PathologyReport


@admin.register(PathologyReport)
class PathologyReportAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'specimen_type', 'collection_date', 'report_date', 
                    'pathologist', 'final_diagnosis']
    list_filter = ['specimen_type', 'collection_date', 'report_date', 'pathologist']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'specimen_type', 'final_diagnosis']
    date_hierarchy = 'report_date'
    ordering = ['-report_date']
