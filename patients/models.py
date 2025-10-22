"""
مدل‌های مربوط به بیماران و بیمه
Patients & Insurance Models
"""
from django.db import models
import uuid


class Patient(models.Model):
    """
    جدول بیماران - اطلاعات دموگرافیک و پایه
    Patients Table - Demographics and Basic Information
    """
    GENDER_CHOICES = [
        ('Male', 'مرد'),
        ('Female', 'زن'),
        ('Other', 'سایر'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    patient_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='شناسه بیمار'
    )
    national_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='کد ملی'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی'
    )
    date_of_birth = models.DateField(
        verbose_name='تاریخ تولد'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='جنسیت'
    )
    primary_phone_number = models.CharField(
        max_length=20,
        verbose_name='شماره تلفن اصلی'
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ایمیل'
    )
    address = models.TextField(
        verbose_name='آدرس منزل'
    )
    emergency_contact_name = models.CharField(
        max_length=200,
        verbose_name='نام مخاطب اضطراری'
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        verbose_name='تلفن مخاطب اضطراری'
    )
    blood_type = models.CharField(
        max_length=5,
        choices=BLOOD_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='گروه خونی'
    )
    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت‌نام'
    )
    
    class Meta:
        verbose_name = 'بیمار'
        verbose_name_plural = 'بیماران'
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"


class Insurance(models.Model):
    """
    جدول بیمه - بیماران می‌توانند چند بیمه داشته باشند
    Insurance Table - Patients can have multiple insurances
    """
    INSURANCE_TYPE_CHOICES = [
        ('Primary', 'پایه'),
        ('Supplementary', 'تکمیلی'),
    ]
    
    insurance_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه بیمه'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='insurances',
        verbose_name='بیمار'
    )
    provider_name = models.CharField(
        max_length=100,
        verbose_name='نام شرکت بیمه'
    )
    policy_number = models.CharField(
        max_length=100,
        verbose_name='شماره بیمه‌نامه'
    )
    group_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='شماره گروه'
    )
    expiry_date = models.DateField(
        verbose_name='تاریخ انقضا'
    )
    insurance_type = models.CharField(
        max_length=20,
        choices=INSURANCE_TYPE_CHOICES,
        verbose_name='نوع بیمه'
    )
    
    class Meta:
        verbose_name = 'بیمه'
        verbose_name_plural = 'بیمه‌ها'
        ordering = ['-expiry_date']
    
    def __str__(self):
        return f"{self.provider_name} - {self.policy_number}"
