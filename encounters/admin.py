from django.contrib import admin
from .models import Encounter, Admission, Appointment


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider', 'encounter_date', 'encounter_type', 'location', 'is_active']
    list_filter = ['encounter_type', 'is_active', 'encounter_date', 'location']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'chief_complaint']
    date_hierarchy = 'encounter_date'
    ordering = ['-encounter_date']


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'admission_date', 'discharge_date', 'admitting_provider', 'current_room', 'discharge_disposition']
    list_filter = ['discharge_disposition', 'admission_date', 'discharge_date']
    search_fields = ['encounter__patient__national_id', 'encounter__patient__first_name', 'encounter__patient__last_name']
    date_hierarchy = 'admission_date'
    ordering = ['-admission_date']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'provider', 'appointment_start_time', 'appointment_status', 'location']
    list_filter = ['appointment_status', 'appointment_start_time', 'location']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'reason_for_visit']
    date_hierarchy = 'appointment_start_time'
    ordering = ['appointment_start_time']
