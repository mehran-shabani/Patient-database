"""
مدل‌های مربوط به پاتولوژی
Pathology Models
"""
from django.db import models


class PathologyReport(models.Model):
    """
    جدول گزارش‌های پاتولوژی - نتایج بیوپسی و نمونه‌برداری
    Pathology Reports Table - Biopsy and specimen results
    """
    pathology_report_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه گزارش پاتولوژی'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='pathology_reports',
        verbose_name='دستور'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='pathology_reports',
        verbose_name='ویزیت'
    )
    specimen_type = models.CharField(
        max_length=100,
        verbose_name='نوع نمونه',
        help_text='مثال: Biopsy, Left Breast Mass'
    )
    collection_date = models.DateTimeField(
        verbose_name='تاریخ نمونه‌برداری'
    )
    pathologist = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='pathology_reports',
        verbose_name='پاتولوژیست',
        limit_choices_to={'provider_type': 'Pathologist'}
    )
    report_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ تایید گزارش'
    )
    macroscopic_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توصیف ماکروسکوپی',
        help_text='توصیف چیزی که با چشم دیده می‌شود'
    )
    microscopic_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توصیف میکروسکوپی',
        help_text='توصیف نمونه تحت میکروسکوپ'
    )
    final_diagnosis = models.TextField(
        blank=True,
        null=True,
        verbose_name='تشخیص نهایی پاتولوژی',
        help_text='مثال: Invasive Ductal Carcinoma'
    )
    additional_tests = models.TextField(
        blank=True,
        null=True,
        verbose_name='تست‌های اضافی',
        help_text='مثال: Immunohistochemistry, Molecular tests'
    )
    
    class Meta:
        verbose_name = 'گزارش پاتولوژی'
        verbose_name_plural = 'گزارش‌های پاتولوژی'
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.specimen_type} ({self.collection_date.strftime('%Y/%m/%d')})"
