"""
مدل‌های مربوط به تشخیص‌ها
Diagnoses Models
"""
from django.db import models


class Diagnosis(models.Model):
    """
    جدول تشخیص‌ها - تشخیص پزشک در یک ویزیت
    Diagnoses Table - Doctor's diagnosis in a visit
    """
    diagnosis_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه تشخیص'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name='ویزیت'
    )
    diagnosis_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='کد تشخیص',
        help_text='کد استاندارد ICD-10'
    )
    diagnosis_description = models.TextField(
        verbose_name='شرح تشخیص'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='تشخیص اصلی'
    )
    diagnosed_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='diagnoses',
        verbose_name='تشخیص دهنده'
    )
    diagnosis_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ تشخیص'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'تشخیص'
        verbose_name_plural = 'تشخیص‌ها'
        ordering = ['-is_primary', '-diagnosis_date']
    
    def __str__(self):
        primary_str = " (اصلی)" if self.is_primary else ""
        return f"{self.encounter.patient} - {self.diagnosis_description[:50]}{primary_str}"
