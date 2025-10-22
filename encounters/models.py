"""
مدل‌های مربوط به ملاقات‌ها، پذیرش و نوبت‌دهی
Encounters, Admissions and Appointments Models
"""
from django.db import models
import uuid


class Encounter(models.Model):
    """
    جدول ملاقات‌ها/ویزیت‌ها - هر بار مراجعه بیمار به مرکز درمانی
    Encounters Table - Each patient visit to healthcare facility
    """
    ENCOUNTER_TYPE_CHOICES = [
        ('Outpatient', 'سرپایی'),
        ('Inpatient', 'بستری'),
        ('Emergency', 'اورژانس'),
        ('Consultation', 'مشاوره'),
    ]
    
    encounter_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='شناسه ویزیت'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='encounters',
        verbose_name='بیمار'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='encounters',
        verbose_name='پزشک معالج'
    )
    encounter_date = models.DateTimeField(
        verbose_name='تاریخ و زمان ویزیت'
    )
    encounter_type = models.CharField(
        max_length=50,
        choices=ENCOUNTER_TYPE_CHOICES,
        verbose_name='نوع مراجعه'
    )
    chief_complaint = models.TextField(
        verbose_name='شکایت اصلی بیمار'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='بخش یا کلینیک'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )
    
    class Meta:
        verbose_name = 'ویزیت'
        verbose_name_plural = 'ویزیت‌ها'
        ordering = ['-encounter_date']
    
    def __str__(self):
        return f"{self.patient} - {self.encounter_date.strftime('%Y/%m/%d %H:%M')} - {self.get_encounter_type_display()}"


class Admission(models.Model):
    """
    جدول پذیرش و بستری - اطلاعات مربوط به بستری شدن بیمار
    Admissions Table - Information about patient hospitalization
    """
    DISCHARGE_DISPOSITION_CHOICES = [
        ('Home', 'مرخص به منزل'),
        ('Transferred', 'انتقال به مرکز دیگر'),
        ('Deceased', 'فوت'),
        ('Left_AMA', 'ترک با رضایت شخصی'),
    ]
    
    admission_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه پذیرش'
    )
    encounter = models.OneToOneField(
        Encounter,
        on_delete=models.CASCADE,
        related_name='admission',
        verbose_name='ویزیت',
        limit_choices_to={'encounter_type': 'Inpatient'}
    )
    admission_date = models.DateTimeField(
        verbose_name='تاریخ و زمان پذیرش'
    )
    discharge_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ و زمان ترخیص'
    )
    admitting_provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='admissions',
        verbose_name='پزشک پذیرش دهنده'
    )
    discharge_provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='discharges',
        blank=True,
        null=True,
        verbose_name='پزشک دستور دهنده ترخیص'
    )
    current_room = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='شماره اتاق فعلی'
    )
    current_bed = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='شماره تخت فعلی'
    )
    admission_diagnosis = models.TextField(
        verbose_name='تشخیص زمان پذیرش'
    )
    discharge_diagnosis = models.TextField(
        blank=True,
        null=True,
        verbose_name='تشخیص نهایی زمان ترخیص'
    )
    discharge_disposition = models.CharField(
        max_length=50,
        choices=DISCHARGE_DISPOSITION_CHOICES,
        blank=True,
        null=True,
        verbose_name='وضعیت ترخیص'
    )
    
    class Meta:
        verbose_name = 'پذیرش'
        verbose_name_plural = 'پذیرش‌ها'
        ordering = ['-admission_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - پذیرش {self.admission_date.strftime('%Y/%m/%d')}"


class Appointment(models.Model):
    """
    جدول نوبت‌دهی - مدیریت نوبت‌های آینده بیماران
    Appointments Table - Managing future patient appointments
    """
    APPOINTMENT_STATUS_CHOICES = [
        ('Scheduled', 'زمان‌بندی شده'),
        ('Completed', 'انجام شده'),
        ('Canceled', 'لغو شده'),
        ('NoShow', 'عدم حضور'),
        ('Rescheduled', 'زمان‌بندی مجدد'),
    ]
    
    appointment_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه نوبت'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='بیمار'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='پزشک'
    )
    appointment_start_time = models.DateTimeField(
        verbose_name='زمان شروع نوبت'
    )
    appointment_end_time = models.DateTimeField(
        verbose_name='زمان پایان نوبت'
    )
    location = models.CharField(
        max_length=100,
        verbose_name='محل'
    )
    appointment_status = models.CharField(
        max_length=20,
        choices=APPOINTMENT_STATUS_CHOICES,
        default='Scheduled',
        verbose_name='وضعیت نوبت'
    )
    reason_for_visit = models.TextField(
        blank=True,
        null=True,
        verbose_name='دلیل مراجعه'
    )
    linked_encounter = models.ForeignKey(
        Encounter,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='appointment',
        verbose_name='ویزیت مرتبط'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )
    
    class Meta:
        verbose_name = 'نوبت'
        verbose_name_plural = 'نوبت‌ها'
        ordering = ['appointment_start_time']
    
    def __str__(self):
        return f"{self.patient} - {self.appointment_start_time.strftime('%Y/%m/%d %H:%M')} - {self.get_appointment_status_display()}"
