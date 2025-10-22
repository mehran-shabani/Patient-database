"""
مدل‌های مربوط به تصویربرداری
Imaging Models
"""
from django.db import models


class ImagingResult(models.Model):
    """
    جدول نتایج تصویربرداری - X-ray, CT, MRI, سونوگرافی و غیره
    Imaging Results Table - X-ray, CT, MRI, Ultrasound, etc.
    """
    MODALITY_CHOICES = [
        ('X-Ray', 'اشعه ایکس'),
        ('CT', 'سی‌تی اسکن'),
        ('MRI', 'ام‌آر‌آی'),
        ('Ultrasound', 'سونوگرافی'),
        ('Mammography', 'ماموگرافی'),
        ('PET', 'پت اسکن'),
        ('Fluoroscopy', 'فلوروسکوپی'),
        ('Other', 'سایر'),
    ]
    
    imaging_result_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه نتیجه تصویربرداری'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='imaging_results',
        verbose_name='دستور',
        limit_choices_to={'order_type': 'Imaging'}
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='imaging_results',
        verbose_name='ویزیت'
    )
    modality = models.CharField(
        max_length=20,
        choices=MODALITY_CHOICES,
        verbose_name='نوع تصویربرداری'
    )
    body_part = models.CharField(
        max_length=100,
        verbose_name='عضو مورد بررسی',
        help_text='مثال: Chest, Head, Abdomen'
    )
    radiologist = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='imaging_reports',
        verbose_name='رادیولوژیست',
        limit_choices_to={'provider_type': 'Radiologist'}
    )
    report_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='زمان تایید گزارش'
    )
    report_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='متن گزارش (Findings)'
    )
    impressions = models.TextField(
        blank=True,
        null=True,
        verbose_name='نتیجه‌گیری نهایی (Impression)'
    )
    pacs_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='لینک تصویر در سیستم PACS',
        help_text='لینک به فایل تصویر در سیستم آرشیو'
    )
    imaging_date = models.DateTimeField(
        verbose_name='تاریخ تصویربرداری'
    )
    
    class Meta:
        verbose_name = 'نتیجه تصویربرداری'
        verbose_name_plural = 'نتایج تصویربرداری'
        ordering = ['-imaging_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.get_modality_display()} {self.body_part} ({self.imaging_date.strftime('%Y/%m/%d')})"
