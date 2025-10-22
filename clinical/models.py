"""
مدل‌های مربوط به اطلاعات بالینی
Clinical Information Models
"""
from django.db import models


class MedicalHistory(models.Model):
    """
    جدول سوابق پزشکی - بیماری‌های مزمن، آلرژی‌ها، جراحی‌های قبلی
    Medical History Table - Chronic diseases, allergies, previous surgeries
    """
    HISTORY_TYPE_CHOICES = [
        ('Allergy', 'آلرژی'),
        ('ChronicCondition', 'بیماری مزمن'),
        ('Surgery', 'جراحی'),
        ('Medication', 'دارویی'),
        ('Other', 'سایر'),
    ]
    
    history_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه سابقه'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='medical_histories',
        verbose_name='بیمار'
    )
    history_type = models.CharField(
        max_length=50,
        choices=HISTORY_TYPE_CHOICES,
        verbose_name='نوع سابقه'
    )
    description = models.TextField(
        verbose_name='شرح'
    )
    onset_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ شروع یا تشخیص'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )
    
    class Meta:
        verbose_name = 'سابقه پزشکی'
        verbose_name_plural = 'سوابق پزشکی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient} - {self.get_history_type_display()}: {self.description[:50]}"


class ProblemList(models.Model):
    """
    جدول لیست مشکلات - مشکلات فعال و مزمن بیمار
    Problem List Table - Active and chronic patient problems
    """
    PROBLEM_STATUS_CHOICES = [
        ('Active', 'فعال'),
        ('Resolved', 'حل شده'),
        ('Chronic', 'مزمن'),
        ('Intermittent', 'متناوب'),
    ]
    
    problem_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه مشکل'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='problems',
        verbose_name='بیمار'
    )
    problem_name = models.CharField(
        max_length=500,
        verbose_name='نام مشکل'
    )
    icd10_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='کد ICD-10'
    )
    onset_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ شروع'
    )
    resolution_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاریخ حل شدن'
    )
    problem_status = models.CharField(
        max_length=20,
        choices=PROBLEM_STATUS_CHOICES,
        default='Active',
        verbose_name='وضعیت مشکل'
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'مشکل'
        verbose_name_plural = 'لیست مشکلات'
        ordering = ['problem_status', '-onset_date']
    
    def __str__(self):
        return f"{self.patient} - {self.problem_name} ({self.get_problem_status_display()})"


class Allergy(models.Model):
    """
    جدول آلرژی‌ها - ساختاریافته‌تر از سابقه پزشکی
    Allergies Table - More structured than medical history
    """
    SUBSTANCE_TYPE_CHOICES = [
        ('Drug', 'دارو'),
        ('Food', 'غذا'),
        ('Environment', 'محیطی'),
        ('Other', 'سایر'),
    ]
    
    SEVERITY_CHOICES = [
        ('Mild', 'خفیف'),
        ('Moderate', 'متوسط'),
        ('Severe', 'شدید'),
        ('Life-Threatening', 'تهدید کننده حیات'),
    ]
    
    VERIFICATION_STATUS_CHOICES = [
        ('Suspected', 'مشکوک'),
        ('Confirmed', 'تایید شده'),
        ('Refuted', 'رد شده'),
    ]
    
    allergy_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه آلرژی'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='allergies',
        verbose_name='بیمار'
    )
    substance = models.CharField(
        max_length=200,
        verbose_name='ماده حساسیت‌زا'
    )
    substance_type = models.CharField(
        max_length=50,
        choices=SUBSTANCE_TYPE_CHOICES,
        verbose_name='نوع ماده'
    )
    reaction = models.TextField(
        verbose_name='شرح واکنش'
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        verbose_name='شدت'
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='Suspected',
        verbose_name='وضعیت تایید'
    )
    recorded_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )
    
    class Meta:
        verbose_name = 'آلرژی'
        verbose_name_plural = 'آلرژی‌ها'
        ordering = ['-severity', '-recorded_date']
    
    def __str__(self):
        return f"{self.patient} - آلرژی به {self.substance} ({self.get_severity_display()})"


class FamilyHistory(models.Model):
    """
    جدول سابقه خانوادگی - اطلاعات حیاتی برای ارزیابی ریسک ژنتیکی
    Family History Table - Vital information for genetic risk assessment
    """
    RELATION_CHOICES = [
        ('Mother', 'مادر'),
        ('Father', 'پدر'),
        ('Sibling', 'خواهر/برادر'),
        ('MaternalGrandmother', 'مادربزرگ مادری'),
        ('MaternalGrandfather', 'پدربزرگ مادری'),
        ('PaternalGrandmother', 'مادربزرگ پدری'),
        ('PaternalGrandfather', 'پدربزرگ پدری'),
        ('Aunt', 'عمه/خاله'),
        ('Uncle', 'عمو/دایی'),
        ('Child', 'فرزند'),
        ('Other', 'سایر'),
    ]
    
    family_history_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه سابقه خانوادگی'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='family_histories',
        verbose_name='بیمار'
    )
    relation = models.CharField(
        max_length=50,
        choices=RELATION_CHOICES,
        verbose_name='نسبت'
    )
    condition = models.CharField(
        max_length=200,
        verbose_name='بیماری یا وضعیت'
    )
    age_of_onset = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='سن شروع بیماری'
    )
    is_deceased = models.BooleanField(
        default=False,
        verbose_name='فوت شده'
    )
    cause_of_death = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='علت فوت'
    )
    
    class Meta:
        verbose_name = 'سابقه خانوادگی'
        verbose_name_plural = 'سوابق خانوادگی'
        ordering = ['relation']
    
    def __str__(self):
        return f"{self.patient} - {self.get_relation_display()}: {self.condition}"


class SocialHistory(models.Model):
    """
    جدول سابقه اجتماعی - عوامل سبک زندگی
    Social History Table - Lifestyle factors
    """
    ITEM_NAME_CHOICES = [
        ('SmokingStatus', 'وضعیت سیگار'),
        ('AlcoholUse', 'مصرف الکل'),
        ('DrugUse', 'مصرف مواد'),
        ('Occupation', 'شغل'),
        ('Exercise', 'ورزش'),
        ('Diet', 'رژیم غذایی'),
        ('MaritalStatus', 'وضعیت تاهل'),
        ('LivingSituation', 'وضعیت زندگی'),
        ('Other', 'سایر'),
    ]
    
    STATUS_CHOICES = [
        ('Current', 'فعلی'),
        ('Former', 'سابق'),
        ('Never', 'هرگز'),
    ]
    
    social_history_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه سابقه اجتماعی'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='social_histories',
        verbose_name='بیمار'
    )
    item_name = models.CharField(
        max_length=50,
        choices=ITEM_NAME_CHOICES,
        verbose_name='موضوع'
    )
    item_value = models.CharField(
        max_length=200,
        verbose_name='مقدار'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='وضعیت'
    )
    recorded_date = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ ثبت'
    )
    
    class Meta:
        verbose_name = 'سابقه اجتماعی'
        verbose_name_plural = 'سوابق اجتماعی'
        ordering = ['item_name', '-recorded_date']
    
    def __str__(self):
        return f"{self.patient} - {self.get_item_name_display()}: {self.item_value}"


class Immunization(models.Model):
    """
    جدول واکسیناسیون - ثبت واکسن‌های تزریق شده
    Immunization Table - Record of administered vaccines
    """
    immunization_id = models.AutoField(
        primary_key=True,
        verbose_name='شناسه واکسیناسیون'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='immunizations',
        verbose_name='بیمار'
    )
    vaccine_name = models.CharField(
        max_length=100,
        verbose_name='نام واکسن'
    )
    cvx_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='کد CVX'
    )
    administered_date = models.DateTimeField(
        verbose_name='تاریخ تزریق'
    )
    administered_by = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='administered_immunizations',
        verbose_name='تزریق کننده'
    )
    site = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='محل تزریق'
    )
    lot_number = models.CharField(
        max_length=50,
        verbose_name='شماره بچ'
    )
    expiration_date = models.DateField(
        verbose_name='تاریخ انقضا'
    )
    was_refused = models.BooleanField(
        default=False,
        verbose_name='امتناع از دریافت'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت‌ها'
    )
    
    class Meta:
        verbose_name = 'واکسیناسیون'
        verbose_name_plural = 'واکسیناسیون‌ها'
        ordering = ['-administered_date']
    
    def __str__(self):
        return f"{self.patient} - {self.vaccine_name} ({self.administered_date.strftime('%Y/%m/%d')})"
