from django.contrib import admin
from .models import MedicalHistory, ProblemList, Allergy, FamilyHistory, SocialHistory, Immunization


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'history_type', 'description', 'onset_date', 'is_active']
    list_filter = ['history_type', 'is_active', 'onset_date']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'description']
    date_hierarchy = 'created_at'


@admin.register(ProblemList)
class ProblemListAdmin(admin.ModelAdmin):
    list_display = ['patient', 'problem_name', 'icd10_code', 'problem_status', 'onset_date', 'resolution_date']
    list_filter = ['problem_status', 'onset_date']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'problem_name', 'icd10_code']


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ['patient', 'substance', 'substance_type', 'severity', 'verification_status', 'recorded_date']
    list_filter = ['substance_type', 'severity', 'verification_status']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'substance', 'reaction']
    date_hierarchy = 'recorded_date'


@admin.register(FamilyHistory)
class FamilyHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'relation', 'condition', 'age_of_onset', 'is_deceased']
    list_filter = ['relation', 'is_deceased']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'condition']


@admin.register(SocialHistory)
class SocialHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'item_name', 'item_value', 'status', 'recorded_date']
    list_filter = ['item_name', 'status']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'item_value']
    date_hierarchy = 'recorded_date'


@admin.register(Immunization)
class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'vaccine_name', 'administered_date', 'administered_by', 'lot_number', 'was_refused']
    list_filter = ['vaccine_name', 'administered_date', 'was_refused']
    search_fields = ['patient__national_id', 'patient__first_name', 'patient__last_name', 'vaccine_name', 'lot_number']
    date_hierarchy = 'administered_date'
