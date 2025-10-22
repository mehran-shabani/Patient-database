"""
مدل‌های مربوط به پروسیجرها و اعمال جراحی
Procedures and Surgeries Models
"""
from django.db import models


class Procedure(models.Model):
    """
    جدول پروسیجرها و اعمال جراحی
    Procedures Table - From simple sutures to major surgeries
    """
    procedure_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه پروسیجر'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='procedures',
        verbose_name='ویزیت'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='procedures',
        verbose_name='دستور',
        limit_choices_to={'order_type': 'Procedure'}
    )
    procedure_name = models.CharField(
        max_length=300,
        verbose_name='نام عمل',
        help_text='مثال: Appendectomy, Bronchoscopy'
    )
    procedure_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='کد استاندارد عمل',
        help_text='کد CPT یا ICD-10-PCS'
    )
    procedure_date = models.DateTimeField(
        verbose_name='تاریخ و زمان شروع عمل'
    )
    primary_surgeon = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='primary_surgeries',
        verbose_name='جراح اصلی'
    )
    anesthesiologist = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='anesthesia_procedures',
        verbose_name='متخصص بیهوشی',
        limit_choices_to={'provider_type': 'Anesthesiologist'}
    )
    procedure_report = models.TextField(
        blank=True,
        null=True,
        verbose_name='گزارش کامل عمل'
    )
    complications = models.TextField(
        blank=True,
        null=True,
        verbose_name='عوارض حین یا پس از عمل'
    )
    duration_minutes = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='مدت زمان عمل (دقیقه)'
    )
    is_emergency = models.BooleanField(
        default=False,
        verbose_name='اورژانسی'
    )
    
    class Meta:
        verbose_name = 'پروسیجر/عمل'
        verbose_name_plural = 'پروسیجرها و اعمال'
        ordering = ['-procedure_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.procedure_name} ({self.procedure_date.strftime('%Y/%m/%d')})"


class ConsentForm(models.Model):
    """
    جدول رضایت‌نامه‌ها - ثبت رضایت‌نامه‌های قانونی و بالینی
    Consent Forms Table - Legal and clinical consent records
    """
    CONSENT_STATUS_CHOICES = [
        ('Signed', 'امضا شده'),
        ('Revoked', 'لغو شده'),
        ('Pending', 'در انتظار'),
    ]
    
    consent_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه رضایت‌نامه'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='consent_forms',
        verbose_name='بیمار'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='consent_forms',
        verbose_name='ویزیت مرتبط'
    )
    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='consent_forms',
        verbose_name='پروسیجر مرتبط'
    )
    consent_type = models.CharField(
        max_length=100,
        verbose_name='نوع رضایت‌نامه',
        help_text='مثال: General Treatment, Surgery, Blood Transfusion'
    )
    consent_status = models.CharField(
        max_length=20,
        choices=CONSENT_STATUS_CHOICES,
        default='Pending',
        verbose_name='وضعیت رضایت‌نامه'
    )
    sign_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ امضا'
    )
    scanned_form_path = models.FileField(
        upload_to='consent_forms/',
        blank=True,
        null=True,
        verbose_name='فایل اسکن شده رضایت‌نامه'
    )
    witnessed_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='witnessed_consents',
        verbose_name='شاهد امضا'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'رضایت‌نامه'
        verbose_name_plural = 'رضایت‌نامه‌ها'
        ordering = ['-sign_timestamp']
    
    def __str__(self):
        return f"{self.patient} - {self.consent_type} ({self.get_consent_status_display()})"
