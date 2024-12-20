

# Register your models here.
from django.contrib import admin
from .models import Role, User, MedicalStaff, Education, Patient, AppointmentType, RecordStatus, MedicalCard, \
    MedicalRecord, UserActionLog


# Регистрация модели Role
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'permission')
    search_fields = ('name',)

admin.site.register(Role, RoleAdmin)

# Регистрация модели User
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'login', 'role')
    search_fields = ('login', 'first_name', 'last_name')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)

# Регистрация модели MedicalStaff
class MedicalStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__login',)

admin.site.register(MedicalStaff, MedicalStaffAdmin)

# Регистрация модели Education
class EducationAdmin(admin.ModelAdmin):
    list_display = ('medical_staff', 'document', 'academic_degree')
    search_fields = ('medical_staff__user__login', 'academic_degree')

admin.site.register(Education, EducationAdmin)

# Регистрация модели Patient
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__login',)

admin.site.register(Patient, PatientAdmin)

# Регистрация модели AppointmentType
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(AppointmentType, AppointmentTypeAdmin)

# Регистрация модели RecordStatus
class RecordStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(RecordStatus, RecordStatusAdmin)

# Регистрация модели MedicalCard
class MedicalCardAdmin(admin.ModelAdmin):
    list_display = ('patient', 'snils_number', 'insurance_policy_number')
    search_fields = ('patient__user__login',)

admin.site.register(MedicalCard, MedicalCardAdmin)

# Регистрация модели MedicalRecord
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('medical_card', 'doctor', 'date', 'diagnosis', 'appointment_type', 'record_status')
    search_fields = ('medical_card__patient__user__login', 'doctor__user__login')

admin.site.register(MedicalRecord, MedicalRecordAdmin)

