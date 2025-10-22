from django.contrib import admin
from .models import CareTeam, CarePlan


@admin.register(CareTeam)
class CareTeamAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider', 'role', 'is_active', 'assigned_date', 'end_date']
    list_filter = ['role', 'is_active', 'assigned_date']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 
                     'provider__first_name', 'provider__last_name']
    date_hierarchy = 'assigned_date'
    ordering = ['-assigned_date']


@admin.register(CarePlan)
class CarePlanAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'category', 'goal', 'status', 'created_by', 'target_date']
    list_filter = ['category', 'status', 'created_date', 'target_date']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 
                     'encounter__patient__last_name', 'goal', 'intervention']
    date_hierarchy = 'created_date'
    ordering = ['-created_date']
