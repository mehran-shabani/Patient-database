"""
مدل‌های مربوط به مدیریت مراقبت
Care Management Models
"""
from django.db import models


class CareTeam(models.Model):
    """
    جدول تیم درمان - در یک ویزیت چه کسانی مسئول بیمار هستند
    Care Team Table - Who is responsible for the patient in a visit
    """
    ROLE_CHOICES = [
        ('AttendingPhysician', 'پزشک معالج'),
        ('Consultant', 'پزشک مشاور'),
        ('PrimaryNurse', 'پرستار اصلی'),
        ('CaseManager', 'مدیر پرونده'),
        ('SocialWorker', 'مددکار اجتماعی'),
        ('Dietitian', 'متخصص تغذیه'),
        ('PhysicalTherapist', 'فیزیوتراپیست'),
        ('Pharmacist', 'داروساز'),
        ('Other', 'سایر'),
    ]
    
    care_team_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه تیم درمان'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='care_team_members',
        verbose_name='ویزیت'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='care_teams',
        verbose_name='بیمار'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='care_team_assignments',
        verbose_name='عضو تیم درمان'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        verbose_name='نقش'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
        help_text='آیا این فرد در حال حاضر فعال است؟'
    )
    assigned_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ اختصاص'
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ پایان'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'عضو تیم درمان'
        verbose_name_plural = 'تیم درمان'
        ordering = ['is_active', '-assigned_date']
    
    def __str__(self):
        active_str = " (فعال)" if self.is_active else " (غیرفعال)"
        return f"{self.patient} - {self.provider} ({self.get_role_display()}){active_str}"


class CarePlan(models.Model):
    """
    جدول برنامه مراقبت - اهداف، مداخلات و برنامه‌های آموزشی
    Care Plan Table - Goals, interventions and educational programs
    """
    CATEGORY_CHOICES = [
        ('Nursing', 'پرستاری'),
        ('DischargePlan', 'برنامه ترخیص'),
        ('Nutrition', 'تغذیه'),
        ('Medication', 'دارویی'),
        ('Education', 'آموزشی'),
        ('Psychosocial', 'روانی-اجتماعی'),
        ('Rehabilitation', 'توانبخشی'),
        ('Other', 'سایر'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'فعال'),
        ('Achieved', 'محقق شده'),
        ('Revised', 'تجدید نظر شده'),
        ('Canceled', 'لغو شده'),
    ]
    
    care_plan_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه برنامه مراقبت'
    )
    encounter = models.ForeignKey(
        'encounters.Encounter',
        on_delete=models.CASCADE,
        related_name='care_plans',
        verbose_name='ویزیت'
    )
    problem = models.ForeignKey(
        'clinical.ProblemList',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='care_plans',
        verbose_name='مشکل مرتبط'
    )
    created_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='created_care_plans',
        verbose_name='ایجاد کننده'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name='دسته‌بندی'
    )
    goal = models.TextField(
        verbose_name='هدف',
        help_text='مثال: بیمار بتواند قند خون خود را مستقل چک کند'
    )
    intervention = models.TextField(
        verbose_name='مداخله',
        help_text='مثال: آموزش استفاده از گلوکومتر'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active',
        verbose_name='وضعیت'
    )
    target_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ هدف'
    )
    evaluation_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌های ارزیابی'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )
    
    class Meta:
        verbose_name = 'برنامه مراقبت'
        verbose_name_plural = 'برنامه‌های مراقبت'
        ordering = ['-status', '-created_date']
    
    def __str__(self):
        return f"{self.encounter.patient} - {self.get_category_display()}: {self.goal[:50]} ({self.get_status_display()})"
