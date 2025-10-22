"""
مدل‌های مربوط به دستورات پزشکی
Medical Orders Models
"""
from django.db import models
import uuid


class Order(models.Model):
    """
    جدول دستورات پزشکی - هر اقدامی در بیمارستان با دستور شروع می‌شود
    Orders Table - Every action in hospital starts with an order
    """
    ORDER_TYPE_CHOICES = [
        ('Medication', 'دارو'),
        ('Lab', 'آزمایش'),
        ('Imaging', 'تصویربرداری'),
        ('Procedure', 'پروسیجر'),
        ('Consult', 'مشاوره'),
        ('Diet', 'رژیم غذایی'),
        ('Other', 'سایر'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('Pending', 'در انتظار'),
        ('InProgress', 'در حال انجام'),
        ('Complete', 'انجام شده'),
        ('Canceled', 'لغو شده'),
        ('Held', 'متوقف شده'),
    ]
    
    PRIORITY_CHOICES = [
        ('STAT', 'فوری'),
        ('ASAP', 'در اسرع وقت'),
        ('Routine', 'معمولی'),
    ]
    
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='شناسه دستور'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='ویزیت'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='بیمار'
    )
    ordered_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='دستور دهنده'
    )
    order_type = models.CharField(
        max_length=50,
        choices=ORDER_TYPE_CHOICES,
        verbose_name='نوع دستور'
    )
    order_description = models.TextField(
        verbose_name='شرح دستور'
    )
    order_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان صدور دستور'
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='Pending',
        verbose_name='وضعیت دستور'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Routine',
        verbose_name='اولویت'
    )
    reason_for_order = models.TextField(
        blank=True,
        null=True,
        verbose_name='دلیل دستور'
    )
    completed_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='زمان انجام'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'دستور پزشکی'
        verbose_name_plural = 'دستورات پزشکی'
        ordering = ['-order_timestamp']
        indexes = [
            models.Index(fields=['order_status', '-order_timestamp']),
            models.Index(fields=['priority', '-order_timestamp']),
        ]
    
    def __str__(self):
        return f"{self.patient} - {self.get_order_type_display()}: {self.order_description[:50]} ({self.get_order_status_display()})"
