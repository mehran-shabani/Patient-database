"""
مدل‌های مربوط به کادر درمان
Healthcare Providers Models
"""
from django.db import models
import uuid


class Provider(models.Model):
    """
    جدول کادر درمان - پزشکان، پرستاران و سایر کارکنان درمانی
    Providers Table - Doctors, Nurses and Other Healthcare Staff
    """
    PROVIDER_TYPE_CHOICES = [
        ('Doctor', 'پزشک'),
        ('Nurse', 'پرستار'),
        ('Technician', 'تکنسین'),
        ('Pharmacist', 'داروساز'),
        ('Radiologist', 'رادیولوژیست'),
        ('Pathologist', 'پاتولوژیست'),
        ('Anesthesiologist', 'متخصص بیهوشی'),
        ('Other', 'سایر'),
    ]
    
    provider_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='شناسه کادر درمان'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی'
    )
    specialty = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='تخصص'
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='شماره نظام پزشکی'
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='شماره تماس کاری'
    )
    provider_type = models.CharField(
        max_length=50,
        choices=PROVIDER_TYPE_CHOICES,
        verbose_name='نوع کادر درمان'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ پیوستن'
    )
    
    class Meta:
        verbose_name = 'کادر درمان'
        verbose_name_plural = 'کادر درمان'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        specialty_str = f" - {self.specialty}" if self.specialty else ""
        return f"{self.get_provider_type_display()} {self.first_name} {self.last_name}{specialty_str}"
