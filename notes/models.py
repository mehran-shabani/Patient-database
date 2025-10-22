"""
مدل‌های مربوط به یادداشت‌های بالینی
Clinical Notes Models
"""
from django.db import models


class ClinicalNote(models.Model):
    """
    جدول یادداشت‌های بالینی - شرح حال، یادداشت‌های پرستاری، خلاصه ترخیص
    Clinical Notes Table - History, nursing notes, discharge summaries
    """
    NOTE_TYPE_CHOICES = [
        ('SOAP', 'شرح حال SOAP'),
        ('Progress', 'یادداشت پیشرفت'),
        ('Nursing', 'یادداشت پرستاری'),
        ('Discharge', 'خلاصه ترخیص'),
        ('Consultation', 'یادداشت مشاوره'),
        ('Admission', 'یادداشت پذیرش'),
        ('Operative', 'گزارش عمل'),
        ('Other', 'سایر'),
    ]
    
    note_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه یادداشت'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='clinical_notes',
        verbose_name='ویزیت'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='clinical_notes',
        verbose_name='نویسنده'
    )
    note_type = models.CharField(
        max_length=50,
        choices=NOTE_TYPE_CHOICES,
        verbose_name='نوع یادداشت'
    )
    note_text = models.TextField(
        verbose_name='متن کامل یادداشت',
        help_text='متن کامل شرح حال، یادداشت یا گزارش'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ثبت یادداشت'
    )
    is_signed = models.BooleanField(
        default=False,
        verbose_name='امضا شده'
    )
    signed_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='زمان امضا'
    )
    amended = models.BooleanField(
        default=False,
        verbose_name='اصلاح شده'
    )
    amendment_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='متن اصلاحیه'
    )
    
    class Meta:
        verbose_name = 'یادداشت بالینی'
        verbose_name_plural = 'یادداشت‌های بالینی'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.get_note_type_display()} ({self.timestamp.strftime('%Y/%m/%d %H:%M')})"
