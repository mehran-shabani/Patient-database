# 🗄️ ساختار دیتابیس سیستم مدیریت بیمارستان

این سند ساختار کامل دیتابیس را به تفکیک اپلیکیشن‌ها و جداول شرح می‌دهد.

## 📊 نمودار روابط (ERD Overview)

```
Patient (بیمار) ──┬── Insurance (بیمه)
                   ├── MedicalHistory (سوابق)
                   ├── Allergy (آلرژی)
                   ├── FamilyHistory (سابقه خانوادگی)
                   ├── ProblemList (لیست مشکلات)
                   ├── Immunization (واکسیناسیون)
                   ├── Appointment (نوبت)
                   └── Encounter (ویزیت) ──┬── Vitals (علائم)
                                            ├── Diagnosis (تشخیص)
                                            ├── Order (دستور)
                                            ├── Medication (دارو)
                                            ├── LabResult (آزمایش)
                                            ├── ImagingResult (تصویربرداری)
                                            ├── Procedure (پروسیجر)
                                            ├── ClinicalNote (یادداشت)
                                            ├── Admission (پذیرش)
                                            └── CarePlan (برنامه مراقبت)

Provider (کادر درمان) ─── مرتبط با همه جداول بالینی
```

---

## 1️⃣ اپلیکیشن: `patients` (بیماران)

### 📋 جدول: Patient (بیمار)
**توضیح**: اطلاعات دموگرافیک و پایه بیماران

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| patient_id | UUID | PK | شناسه یکتای بیمار |
| national_id | VARCHAR(10) | UNIQUE | کد ملی |
| first_name | VARCHAR(100) | - | نام |
| last_name | VARCHAR(100) | - | نام خانوادگی |
| date_of_birth | DATE | - | تاریخ تولد |
| gender | VARCHAR(10) | - | جنسیت (Male/Female/Other) |
| primary_phone_number | VARCHAR(20) | - | شماره تلفن |
| email | EMAIL | - | ایمیل |
| address | TEXT | - | آدرس |
| emergency_contact_name | VARCHAR(200) | - | نام مخاطب اضطراری |
| emergency_contact_phone | VARCHAR(20) | - | تلفن مخاطب اضطراری |
| blood_type | VARCHAR(5) | - | گروه خونی |
| registration_date | DATETIME | - | تاریخ ثبت‌نام |

### 📋 جدول: Insurance (بیمه)
**توضیح**: اطلاعات بیمه بیماران

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| insurance_id | INT | PK | شناسه بیمه |
| patient_id | UUID | FK → Patient | بیمار |
| provider_name | VARCHAR(100) | - | نام شرکت بیمه |
| policy_number | VARCHAR(100) | - | شماره بیمه‌نامه |
| group_number | VARCHAR(50) | - | شماره گروه |
| expiry_date | DATE | - | تاریخ انقضا |
| insurance_type | VARCHAR(20) | - | نوع (Primary/Supplementary) |

---

## 2️⃣ اپلیکیشن: `providers` (کادر درمان)

### 📋 جدول: Provider (کادر درمان)
**توضیح**: اطلاعات پزشکان، پرستاران و کارکنان

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| provider_id | UUID | PK | شناسه کادر درمان |
| first_name | VARCHAR(100) | - | نام |
| last_name | VARCHAR(100) | - | نام خانوادگی |
| specialty | VARCHAR(100) | - | تخصص |
| license_number | VARCHAR(50) | UNIQUE | شماره نظام پزشکی |
| phone_number | VARCHAR(20) | - | شماره تماس |
| provider_type | VARCHAR(50) | - | نوع (Doctor/Nurse/Technician...) |
| is_active | BOOLEAN | - | وضعیت فعال |
| date_joined | DATETIME | - | تاریخ پیوستن |

---

## 3️⃣ اپلیکیشن: `encounters` (ویزیت‌ها)

### 📋 جدول: Encounter (ویزیت)
**توضیح**: ثبت هر بار مراجعه بیمار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| encounter_id | UUID | PK | شناسه ویزیت |
| patient_id | UUID | FK → Patient | بیمار |
| provider_id | UUID | FK → Provider | پزشک معالج |
| encounter_date | DATETIME | - | تاریخ و زمان ویزیت |
| encounter_type | VARCHAR(50) | - | نوع (Outpatient/Inpatient/Emergency) |
| chief_complaint | TEXT | - | شکایت اصلی |
| location | VARCHAR(100) | - | بخش یا کلینیک |
| is_active | BOOLEAN | - | فعال |

### 📋 جدول: Admission (پذیرش)
**توضیح**: اطلاعات بستری بیمار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| admission_id | INT | PK | شناسه پذیرش |
| encounter_id | UUID | FK → Encounter | ویزیت |
| admission_date | DATETIME | - | تاریخ پذیرش |
| discharge_date | DATETIME | - | تاریخ ترخیص |
| admitting_provider_id | UUID | FK → Provider | پزشک پذیرش |
| discharge_provider_id | UUID | FK → Provider | پزشک ترخیص |
| current_room | VARCHAR(20) | - | شماره اتاق |
| current_bed | VARCHAR(10) | - | شماره تخت |
| admission_diagnosis | TEXT | - | تشخیص پذیرش |
| discharge_diagnosis | TEXT | - | تشخیص ترخیص |
| discharge_disposition | VARCHAR(50) | - | وضعیت ترخیص |

### 📋 جدول: Appointment (نوبت)
**توضیح**: مدیریت نوبت‌های آینده

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| appointment_id | INT | PK | شناسه نوبت |
| patient_id | UUID | FK → Patient | بیمار |
| provider_id | UUID | FK → Provider | پزشک |
| appointment_start_time | DATETIME | - | زمان شروع |
| appointment_end_time | DATETIME | - | زمان پایان |
| location | VARCHAR(100) | - | محل |
| appointment_status | VARCHAR(20) | - | وضعیت نوبت |
| reason_for_visit | TEXT | - | دلیل مراجعه |
| linked_encounter_id | UUID | FK → Encounter | ویزیت مرتبط |

---

## 4️⃣ اپلیکیشن: `clinical` (اطلاعات بالینی)

### 📋 جدول: MedicalHistory (سوابق پزشکی)
**توضیح**: بیماری‌های مزمن، جراحی‌های قبلی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| history_id | INT | PK | شناسه سابقه |
| patient_id | UUID | FK → Patient | بیمار |
| history_type | VARCHAR(50) | - | نوع سابقه |
| description | TEXT | - | شرح |
| onset_date | DATE | - | تاریخ شروع |
| is_active | BOOLEAN | - | فعال |

### 📋 جدول: ProblemList (لیست مشکلات)
**توضیح**: مشکلات فعال و مزمن بیمار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| problem_id | INT | PK | شناسه مشکل |
| patient_id | UUID | FK → Patient | بیمار |
| problem_name | VARCHAR(500) | - | نام مشکل |
| icd10_code | VARCHAR(20) | - | کد ICD-10 |
| onset_date | DATE | - | تاریخ شروع |
| resolution_date | DATE | - | تاریخ حل شدن |
| problem_status | VARCHAR(20) | - | وضعیت |
| comments | TEXT | - | یادداشت‌ها |

### 📋 جدول: Allergy (آلرژی)
**توضیح**: آلرژی‌های بیمار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| allergy_id | INT | PK | شناسه آلرژی |
| patient_id | UUID | FK → Patient | بیمار |
| substance | VARCHAR(200) | - | ماده حساسیت‌زا |
| substance_type | VARCHAR(50) | - | نوع (Drug/Food/Environment) |
| reaction | TEXT | - | شرح واکنش |
| severity | VARCHAR(20) | - | شدت |
| verification_status | VARCHAR(20) | - | وضعیت تایید |
| recorded_date | DATETIME | - | تاریخ ثبت |

### 📋 جدول: FamilyHistory (سابقه خانوادگی)
**توضیح**: سوابق بیماری‌های خانوادگی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| family_history_id | INT | PK | شناسه سابقه |
| patient_id | UUID | FK → Patient | بیمار |
| relation | VARCHAR(50) | - | نسبت (Mother/Father/Sibling...) |
| condition | VARCHAR(200) | - | بیماری |
| age_of_onset | INT | - | سن شروع |
| is_deceased | BOOLEAN | - | فوت شده |
| cause_of_death | VARCHAR(200) | - | علت فوت |

### 📋 جدول: SocialHistory (سابقه اجتماعی)
**توضیح**: عوامل سبک زندگی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| social_history_id | INT | PK | شناسه سابقه |
| patient_id | UUID | FK → Patient | بیمار |
| item_name | VARCHAR(50) | - | موضوع (SmokingStatus/Exercise...) |
| item_value | VARCHAR(200) | - | مقدار |
| status | VARCHAR(20) | - | وضعیت (Current/Former/Never) |
| recorded_date | DATETIME | - | تاریخ ثبت |

### 📋 جدول: Immunization (واکسیناسیون)
**توضیح**: ثبت واکسن‌های تزریق شده

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| immunization_id | INT | PK | شناسه واکسن |
| patient_id | UUID | FK → Patient | بیمار |
| vaccine_name | VARCHAR(100) | - | نام واکسن |
| cvx_code | VARCHAR(10) | - | کد CVX |
| administered_date | DATETIME | - | تاریخ تزریق |
| administered_by_id | UUID | FK → Provider | تزریق کننده |
| site | VARCHAR(50) | - | محل تزریق |
| lot_number | VARCHAR(50) | - | شماره بچ |
| expiration_date | DATE | - | تاریخ انقضا |
| was_refused | BOOLEAN | - | امتناع |

---

## 5️⃣ اپلیکیشن: `vitals` (علائم حیاتی)

### 📋 جدول: Vital (علائم حیاتی)
**توضیح**: ثبت علائم حیاتی در هر ویزیت

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| vital_id | INT | PK | شناسه علائم |
| encounter_id | UUID | FK → Encounter | ویزیت |
| timestamp | DATETIME | - | زمان ثبت |
| blood_pressure_systolic | INT | - | فشار خون سیستولیک |
| blood_pressure_diastolic | INT | - | فشار خون دیاستولیک |
| heart_rate | INT | - | ضربان قلب |
| temperature | DECIMAL(4,1) | - | دمای بدن |
| respiratory_rate | INT | - | نرخ تنفس |
| oxygen_saturation | INT | - | اشباع اکسیژن |
| weight_kg | DECIMAL(5,2) | - | وزن |
| height_cm | INT | - | قد |
| recorded_by_id | UUID | FK → Provider | ثبت کننده |

### 📋 جدول: FlowsheetData (فلوشیت)
**توضیح**: ثبت داده‌های سری زمانی (Tall format)

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| flowsheet_entry_id | BIGINT | PK | شناسه فلوشیت |
| encounter_id | UUID | FK → Encounter | ویزیت |
| recorded_by_id | UUID | FK → Provider | ثبت کننده |
| timestamp | DATETIME | - | زمان ثبت |
| flowsheet_item_name | VARCHAR(100) | - | نام آیتم |
| item_value | VARCHAR(100) | - | مقدار |
| units | VARCHAR(20) | - | واحد |

---

## 6️⃣ اپلیکیشن: `diagnostics` (تشخیص‌ها)

### 📋 جدول: Diagnosis (تشخیص)
**توضیح**: تشخیص‌های پزشک

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| diagnosis_id | INT | PK | شناسه تشخیص |
| encounter_id | UUID | FK → Encounter | ویزیت |
| diagnosis_code | VARCHAR(20) | - | کد ICD-10 |
| diagnosis_description | TEXT | - | شرح تشخیص |
| is_primary | BOOLEAN | - | تشخیص اصلی |
| diagnosed_by_id | UUID | FK → Provider | تشخیص دهنده |
| diagnosis_date | DATETIME | - | تاریخ تشخیص |

---

## 7️⃣ اپلیکیشن: `orders` (دستورات)

### 📋 جدول: Order (دستور پزشکی)
**توضیح**: تمام دستورات پزشکی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| order_id | UUID | PK | شناسه دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| patient_id | UUID | FK → Patient | بیمار |
| ordered_by_id | UUID | FK → Provider | دستور دهنده |
| order_type | VARCHAR(50) | - | نوع (Medication/Lab/Imaging...) |
| order_description | TEXT | - | شرح دستور |
| order_timestamp | DATETIME | - | زمان صدور |
| order_status | VARCHAR(20) | - | وضعیت |
| priority | VARCHAR(10) | - | اولویت (STAT/ASAP/Routine) |
| reason_for_order | TEXT | - | دلیل |

---

## 8️⃣ اپلیکیشن: `medications` (داروها)

### 📋 جدول: Medication (نسخه)
**توضیح**: نسخه‌های تجویز شده

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| prescription_id | INT | PK | شناسه نسخه |
| encounter_id | UUID | FK → Encounter | ویزیت |
| provider_id | UUID | FK → Provider | پزشک تجویز کننده |
| medication_name | VARCHAR(200) | - | نام دارو |
| dosage | VARCHAR(100) | - | دوز |
| frequency | VARCHAR(100) | - | تکرار |
| duration_days | INT | - | مدت مصرف |
| instructions | TEXT | - | دستورالعمل |
| refills | INT | - | تعداد تکرار نسخه |
| prescribed_date | DATETIME | - | تاریخ تجویز |
| is_active | BOOLEAN | - | فعال |

### 📋 جدول: MedicationAdministration (اجرای دارو)
**توضیح**: ثبت دادن دارو توسط پرستار (MAR)

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| med_admin_id | INT | PK | شناسه اجرا |
| order_id | UUID | FK → Order | دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| administered_by_id | UUID | FK → Provider | پرستار |
| medication_name | VARCHAR(200) | - | نام دارو |
| administration_time | DATETIME | - | زمان تزریق |
| dosage_given | VARCHAR(50) | - | دوز داده شده |
| route | VARCHAR(20) | - | مسیر (PO/IV/IM/SC...) |
| site | VARCHAR(50) | - | محل تزریق |
| patient_refusal | BOOLEAN | - | امتناع بیمار |

---

## 9️⃣ اپلیکیشن: `laboratory` (آزمایشگاه)

### 📋 جدول: LabResult (نتیجه آزمایش)
**توضیح**: نتایج آزمایش‌های خون و ادرار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| lab_result_id | INT | PK | شناسه نتیجه |
| order_id | UUID | FK → Order | دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| test_name | VARCHAR(100) | - | نام آزمایش |
| result_value | VARCHAR(100) | - | مقدار نتیجه |
| units | VARCHAR(20) | - | واحد |
| reference_range | VARCHAR(50) | - | محدوده نرمال |
| result_date | DATETIME | - | تاریخ آماده شدن |
| status | VARCHAR(20) | - | وضعیت |
| is_abnormal | BOOLEAN | - | غیر طبیعی |
| performed_by_id | UUID | FK → Provider | انجام دهنده |

### 📋 جدول: MicrobiologyResult (میکروبیولوژی)
**توضیح**: نتایج کشت و حساسیت آنتی‌بیوتیکی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| micro_result_id | INT | PK | شناسه نتیجه |
| order_id | UUID | FK → Order | دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| specimen_type | VARCHAR(100) | - | نوع نمونه |
| collection_date | DATETIME | - | تاریخ نمونه‌گیری |
| report_date | DATETIME | - | تاریخ گزارش |
| organism_name | VARCHAR(100) | - | نام ارگانیسم |
| sensitivity_data | JSON | - | آنتی‌بیوگرام |
| microbiologist_id | UUID | FK → Provider | میکروبیولوژیست |

---

## 🔟 اپلیکیشن: `imaging` (تصویربرداری)

### 📋 جدول: ImagingResult (نتیجه تصویربرداری)
**توضیح**: نتایج X-Ray, CT, MRI, سونوگرافی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| imaging_result_id | INT | PK | شناسه نتیجه |
| order_id | UUID | FK → Order | دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| modality | VARCHAR(20) | - | نوع (X-Ray/CT/MRI/Ultrasound) |
| body_part | VARCHAR(100) | - | عضو مورد بررسی |
| radiologist_id | UUID | FK → Provider | رادیولوژیست |
| report_timestamp | DATETIME | - | زمان گزارش |
| report_text | TEXT | - | متن گزارش |
| impressions | TEXT | - | نتیجه‌گیری |
| pacs_link | URL | - | لینک تصویر |
| imaging_date | DATETIME | - | تاریخ تصویربرداری |

---

## 1️⃣1️⃣ اپلیکیشن: `procedures` (پروسیجرها)

### 📋 جدول: Procedure (پروسیجر/عمل)
**توضیح**: اعمال جراحی و پروسیجرها

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| procedure_id | INT | PK | شناسه پروسیجر |
| encounter_id | UUID | FK → Encounter | ویزیت |
| order_id | UUID | FK → Order | دستور |
| procedure_name | VARCHAR(300) | - | نام عمل |
| procedure_code | VARCHAR(50) | - | کد CPT/ICD-10-PCS |
| procedure_date | DATETIME | - | تاریخ عمل |
| primary_surgeon_id | UUID | FK → Provider | جراح اصلی |
| anesthesiologist_id | UUID | FK → Provider | متخصص بیهوشی |
| procedure_report | TEXT | - | گزارش عمل |
| complications | TEXT | - | عوارض |
| duration_minutes | INT | - | مدت زمان |
| is_emergency | BOOLEAN | - | اورژانسی |

### 📋 جدول: ConsentForm (رضایت‌نامه)
**توضیح**: رضایت‌نامه‌های قانونی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| consent_id | INT | PK | شناسه رضایت‌نامه |
| patient_id | UUID | FK → Patient | بیمار |
| encounter_id | UUID | FK → Encounter | ویزیت |
| procedure_id | INT | FK → Procedure | پروسیجر |
| consent_type | VARCHAR(100) | - | نوع رضایت‌نامه |
| consent_status | VARCHAR(20) | - | وضعیت (Signed/Revoked/Pending) |
| sign_timestamp | DATETIME | - | تاریخ امضا |
| scanned_form_path | FILE | - | فایل اسکن شده |
| witnessed_by_id | UUID | FK → Provider | شاهد امضا |

---

## 1️⃣2️⃣ اپلیکیشن: `pathology` (پاتولوژی)

### 📋 جدول: PathologyReport (گزارش پاتولوژی)
**توضیح**: گزارش‌های بیوپسی و نمونه‌برداری

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| pathology_report_id | INT | PK | شناسه گزارش |
| order_id | UUID | FK → Order | دستور |
| encounter_id | UUID | FK → Encounter | ویزیت |
| specimen_type | VARCHAR(100) | - | نوع نمونه |
| collection_date | DATETIME | - | تاریخ نمونه‌برداری |
| pathologist_id | UUID | FK → Provider | پاتولوژیست |
| report_date | DATETIME | - | تاریخ گزارش |
| macroscopic_description | TEXT | - | توصیف ماکروسکوپی |
| microscopic_description | TEXT | - | توصیف میکروسکوپی |
| final_diagnosis | TEXT | - | تشخیص نهایی |
| additional_tests | TEXT | - | تست‌های اضافی |

---

## 1️⃣3️⃣ اپلیکیشن: `notes` (یادداشت‌ها)

### 📋 جدول: ClinicalNote (یادداشت بالینی)
**توضیح**: شرح حال، یادداشت‌های پرستاری، خلاصه ترخیص

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| note_id | INT | PK | شناسه یادداشت |
| encounter_id | UUID | FK → Encounter | ویزیت |
| provider_id | UUID | FK → Provider | نویسنده |
| note_type | VARCHAR(50) | - | نوع (SOAP/Progress/Discharge...) |
| note_text | TEXT | - | متن کامل |
| timestamp | DATETIME | - | زمان ثبت |
| is_signed | BOOLEAN | - | امضا شده |
| signed_timestamp | DATETIME | - | زمان امضا |
| amended | BOOLEAN | - | اصلاح شده |
| amendment_text | TEXT | - | متن اصلاحیه |

---

## 1️⃣4️⃣ اپلیکیشن: `care_management` (مدیریت مراقبت)

### 📋 جدول: CareTeam (تیم درمان)
**توضیح**: اعضای تیم درمان بیمار

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| care_team_id | INT | PK | شناسه تیم |
| encounter_id | UUID | FK → Encounter | ویزیت |
| patient_id | UUID | FK → Patient | بیمار |
| provider_id | UUID | FK → Provider | عضو تیم |
| role | VARCHAR(50) | - | نقش (AttendingPhysician/Nurse...) |
| is_active | BOOLEAN | - | فعال |
| assigned_date | DATETIME | - | تاریخ اختصاص |
| end_date | DATETIME | - | تاریخ پایان |

### 📋 جدول: CarePlan (برنامه مراقبت)
**توضیح**: اهداف و برنامه‌های مراقبتی

| ستون | نوع | کلید | توضیح |
|------|-----|------|-------|
| care_plan_id | INT | PK | شناسه برنامه |
| encounter_id | UUID | FK → Encounter | ویزیت |
| problem_id | INT | FK → ProblemList | مشکل مرتبط |
| created_by_id | UUID | FK → Provider | ایجاد کننده |
| category | VARCHAR(50) | - | دسته‌بندی (Nursing/Education...) |
| goal | TEXT | - | هدف |
| intervention | TEXT | - | مداخله |
| status | VARCHAR(20) | - | وضعیت (Active/Achieved/Canceled) |
| target_date | DATE | - | تاریخ هدف |
| evaluation_notes | TEXT | - | یادداشت‌های ارزیابی |
| created_date | DATETIME | - | تاریخ ایجاد |
| updated_date | DATETIME | - | تاریخ به‌روزرسانی |

---

## 📊 خلاصه آماری

| آیتم | تعداد |
|------|-------|
| **تعداد کل اپلیکیشن‌ها** | 14 |
| **تعداد کل جداول** | 27 |
| **جداول اصلی (Core)** | 3 (Patient, Provider, Encounter) |
| **جداول بالینی** | 24 |

---

## 🔗 روابط کلیدی

### روابط One-to-Many:
- Patient → Insurance (1:N)
- Patient → Encounter (1:N)
- Provider → Encounter (1:N)
- Encounter → Vitals (1:N)
- Encounter → Diagnosis (1:N)
- Encounter → Order (1:N)

### روابط One-to-One:
- Encounter → Admission (1:1)

### روابط Many-to-Many (از طریق جدول واسط):
- Patient ↔ Provider (از طریق Encounter)
- Patient ↔ Provider (از طریق CareTeam)

---

**نکته امنیتی**: تمام جداولی که حاوی اطلاعات حساس بیمار هستند باید از رمزنگاری و کنترل دسترسی مناسب برخوردار باشند.

**استاندارد**: این ساختار با استانداردهای FHIR و HL7 سازگار است.
