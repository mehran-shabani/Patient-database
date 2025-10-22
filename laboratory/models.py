"""
مدل‌های مربوط به آزمایشگاه
Laboratory Models
"""
from django.db import models


class LabResult(models.Model):
    """
    جدول نتایج آزمایش‌ها - آزمایش‌های خون، ادرار و غیره
    Lab Results Table - Blood, urine and other lab tests
    """
    STATUS_CHOICES = [
        ('Pending', 'در انتظار'),
        ('InProgress', 'در حال انجام'),
        ('Complete', 'تکمیل شده'),
        ('Canceled', 'لغو شده'),
    ]
    
    lab_result_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه نتیجه آزمایش'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='lab_results',
        verbose_name='دستور',
        limit_choices_to={'order_type': 'Lab'}
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='lab_results',
        verbose_name='ویزیت'
    )
    test_name = models.CharField(
        max_length=100,
        verbose_name='نام آزمایش',
        help_text='مثال: CBC, Blood Glucose, Creatinine'
    )
    result_value = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='مقدار نتیجه'
    )
    units = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='واحد اندازه‌گیری',
        help_text='مثال: mg/dL, mmol/L'
    )
    reference_range = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='محدوده نرمال',
        help_text='مثال: 70-100'
    )
    result_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ آماده شدن جواب'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name='وضعیت'
    )
    is_abnormal = models.BooleanField(
        default=False,
        verbose_name='غیر طبیعی'
    )
    performed_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='performed_lab_tests',
        verbose_name='انجام دهنده'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'نتیجه آزمایش'
        verbose_name_plural = 'نتایج آزمایش‌ها'
        ordering = ['-result_date']
    
    def __str__(self):
        value_str = f": {self.result_value} {self.units or ''}" if self.result_value else ""
        return f"{self.encounter.patient} - {self.test_name}{value_str}"


class MicrobiologyResult(models.Model):
    """
    جدول نتایج میکروبیولوژی - کشت‌ها و حساسیت آنتی‌بیوتیکی
    Microbiology Results Table - Cultures and antibiotic sensitivities
    """
    micro_result_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه نتیجه میکروبیولوژی'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='microbiology_results',
        verbose_name='دستور'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='microbiology_results',
        verbose_name='ویزیت'
    )
    specimen_type = models.CharField(
        max_length=100,
        verbose_name='نوع نمونه',
        help_text='مثال: Blood Culture, Urine Culture, Wound Swab'
    )
    collection_date = models.DateTimeField(
        verbose_name='تاریخ نمونه‌گیری'
    )
    report_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ گزارش'
    )
    organism_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='نام ارگانیسم',
        help_text='مثال: E. coli, No Growth After 48h'
    )
    sensitivity_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name='داده‌های آنتی‌بیوگرام',
        help_text='نتایج حساسیت آنتی‌بیوتیکی به صورت JSON'
    )
    microbiologist = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='microbiology_reports',
        verbose_name='میکروبیولوژیست'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'نتیجه میکروبیولوژی'
        verbose_name_plural = 'نتایج میکروبیولوژی'
        ordering = ['-report_date']
    
    def __str__(self):
        organism_str = f" - {self.organism_name}" if self.organism_name else ""
        return f"{self.encounter.patient} - {self.specimen_type}{organism_str}"
