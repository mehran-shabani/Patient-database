"""
مدل‌های مربوط به داروها
Medications Models
"""
from django.db import models


class Medication(models.Model):
    """
    جدول داروها - نسخه‌های تجویز شده
    Medications Table - Prescribed medications
    """
    prescription_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه نسخه'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='medications',
        verbose_name='ویزیت'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='prescribed_medications',
        verbose_name='پزشک تجویز کننده'
    )
    medication_name = models.CharField(
        max_length=200,
        verbose_name='نام دارو'
    )
    dosage = models.CharField(
        max_length=100,
        verbose_name='دوز مصرف'
    )
    frequency = models.CharField(
        max_length=100,
        verbose_name='تکرار مصرف',
        help_text='مثال: هر 8 ساعت، روزی 3 بار'
    )
    duration_days = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='مدت زمان مصرف (روز)'
    )
    instructions = models.TextField(
        blank=True,
        null=True,
        verbose_name='دستورالعمل‌های خاص',
        help_text='مثال: بعد از غذا، با آب فراوان'
    )
    refills = models.IntegerField(
        default=0,
        verbose_name='تعداد دفعات مجاز تکرار نسخه'
    )
    prescribed_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ تجویز'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'نسخه دارو'
        verbose_name_plural = 'نسخه‌های دارو'
        ordering = ['-prescribed_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.medication_name} {self.dosage}"


class MedicationAdministration(models.Model):
    """
    جدول اجرای داروها - ثبت لحظه دادن دارو به بیمار (MAR)
    Medication Administration Table - Record of actual drug administration (MAR)
    """
    ROUTE_CHOICES = [
        ('PO', 'خوراکی (Oral)'),
        ('IV', 'داخل وریدی (Intravenous)'),
        ('IM', 'داخل عضلانی (Intramuscular)'),
        ('SC', 'زیر جلدی (Subcutaneous)'),
        ('Topical', 'موضعی'),
        ('Inhalation', 'استنشاقی'),
        ('Rectal', 'رکتال'),
        ('Other', 'سایر'),
    ]
    
    med_admin_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه اجرای دارو'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='medication_administrations',
        verbose_name='دستور',
        limit_choices_to={'order_type': 'Medication'}
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='medication_administrations',
        verbose_name='ویزیت'
    )
    administered_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='administered_medications',
        verbose_name='پرستار اجرا کننده'
    )
    medication_name = models.CharField(
        max_length=200,
        verbose_name='نام دارو'
    )
    administration_time = models.DateTimeField(
        verbose_name='زمان دادن دارو'
    )
    dosage_given = models.CharField(
        max_length=50,
        verbose_name='دوز داده شده'
    )
    route = models.CharField(
        max_length=20,
        choices=ROUTE_CHOICES,
        verbose_name='مسیر دادن دارو'
    )
    site = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='محل تزریق',
        help_text='مثال: بازوی چپ، ران راست'
    )
    patient_refusal = models.BooleanField(
        default=False,
        verbose_name='امتناع بیمار از مصرف'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت پرستار'
    )
    
    class Meta:
        verbose_name = 'اجرای دارو'
        verbose_name_plural = 'اجرای داروها'
        ordering = ['-administration_time']
    
    def __str__(self):
        refusal_str = " (امتناع)" if self.patient_refusal else ""
        return f"{self.encounter.patient} - {self.medication_name} ({self.administration_time.strftime('%Y/%m/%d %H:%M')}){refusal_str}"
