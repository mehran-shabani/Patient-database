"""
مدل‌های مربوط به علائم حیاتی
Vital Signs Models
"""
from django.db import models


class Vital(models.Model):
    """
    جدول علائم حیاتی - در هر ویزیت ثبت می‌شود
    Vitals Table - Recorded at each visit
    """
    vital_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه علائم حیاتی'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='vitals',
        verbose_name='ویزیت'
    )
    timestamp = models.DateTimeField(
        verbose_name='زمان ثبت'
    )
    blood_pressure_systolic = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='فشار خون سیستولیک (بالا)'
    )
    blood_pressure_diastolic = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='فشار خون دیاستولیک (پایین)'
    )
    heart_rate = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='ضربان قلب'
    )
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name='دمای بدن'
    )
    respiratory_rate = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='نرخ تنفس'
    )
    oxygen_saturation = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='اشباع اکسیژن (SpO2)'
    )
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='وزن (کیلوگرم)'
    )
    height_cm = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='قد (سانتی‌متر)'
    )
    recorded_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='recorded_vitals',
        verbose_name='ثبت کننده'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'علائم حیاتی'
        verbose_name_plural = 'علائم حیاتی'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.timestamp.strftime('%Y/%m/%d %H:%M')}"


class FlowsheetData(models.Model):
    """
    جدول فلوشیت‌ها - ثبت تمام داده‌های سری زمانی (Tall/Narrow format)
    Flowsheet Table - Recording all time-series data (Tall/Narrow format)
    """
    flowsheet_entry_id = models.BigAutoField(
        primary_key=True,
        verbose_name='شناسه فلوشیت'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='flowsheet_data',
        verbose_name='ویزیت'
    )
    recorded_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='recorded_flowsheets',
        verbose_name='ثبت کننده'
    )
    timestamp = models.DateTimeField(
        verbose_name='زمان ثبت'
    )
    flowsheet_item_name = models.CharField(
        max_length=100,
        verbose_name='نام آیتم',
        help_text='مثال: HeartRate, PainScore, UrineOutput, GCS_Total'
    )
    item_value = models.CharField(
        max_length=100,
        verbose_name='مقدار آیتم'
    )
    units = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='واحد',
        help_text='مثال: bpm, mL, 1-10'
    )
    
    class Meta:
        verbose_name = 'داده فلوشیت'
        verbose_name_plural = 'داده‌های فلوشیت'
        ordering = ['-timestamp', 'flowsheet_item_name']
        indexes = [
            models.Index(fields=['encounter', 'flowsheet_item_name', '-timestamp']),
        ]
    
    def __str__(self):
        unit_str = f" {self.units}" if self.units else ""
        return f"{self.encounter.patient} - {self.flowsheet_item_name}: {self.item_value}{unit_str} ({self.timestamp.strftime('%Y/%m/%d %H:%M')})"
