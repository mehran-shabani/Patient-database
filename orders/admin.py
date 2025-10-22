from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['patient', 'order_type', 'order_description', 'order_status', 'priority', 
                    'ordered_by', 'order_timestamp']
    list_filter = ['order_type', 'order_status', 'priority', 'order_timestamp']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 
                     'order_description', 'reason_for_order']
    date_hierarchy = 'order_timestamp'
    ordering = ['-order_timestamp']
