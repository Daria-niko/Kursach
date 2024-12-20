from cryptography.fernet import Fernet
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Роли
class Role(models.Model):
    name = models.CharField(max_length=100)
    permission = models.TextField()

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField()
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Сотрудники медорганизации
class MedicalStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medical_staff')
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.user}"


# Образование
class Education(models.Model):
    medical_staff = models.OneToOneField(MedicalStaff, on_delete=models.CASCADE, related_name='education')
    document = models.CharField(max_length=255)
    academic_degree = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medical_staff.user}: {self.academic_degree}"

# Пациенты
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return str(self.user)

# Виды приема
class AppointmentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Статусы записи
class RecordStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

key = b'xgKmqIkcsQpsexVu-1x44yKvIqgJrUgZO9YDh0LzJY0='

cipher = Fernet(key)

# Медицинские карты
class MedicalCard(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_card')
    _snils_number = models.CharField(max_length=255, default='')
    _insurance_policy_number = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        if not self._snils_number.startswith('gAAAA'):  # Проверка на зашифрованность
            self._snils_number = cipher.encrypt(self._snils_number.encode('utf-8')).decode('utf-8')
        if not self._insurance_policy_number.startswith('gAAAA'):
            self._insurance_policy_number = cipher.encrypt(self._insurance_policy_number.encode('utf-8')).decode('utf-8')
        super().save(*args, **kwargs)

    @property
    def encrypted_snils_number(self):
        # Пример шифрования, если используется
        return self.snils_number  # или какое-то шифрование
    @property
    def snils_number(self):
        # Расшифровка данных при доступе
        try:
            return cipher.decrypt(self._snils_number.encode('utf-8')).decode('utf-8')
        except Exception:
            return "Ошибка: невозможно расшифровать СНИЛС"

    @property
    def insurance_policy_number(self):
        # Расшифровка данных при доступе
        try:
            return cipher.decrypt(self._insurance_policy_number.encode('utf-8')).decode('utf-8')
        except Exception:
            return "Ошибка: невозможно расшифровать полис"
    def __str__(self):
        return f"Card for {self.patient.user}"

# Медицинские записи
class MedicalRecord(models.Model):
    medical_card = models.ForeignKey(MedicalCard, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(MedicalStaff, on_delete=models.CASCADE, related_name='medical_records')
    date = models.DateField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(null=True, blank=True)
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE)
    record_status = models.ForeignKey(RecordStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"Record for {self.medical_card.patient.user} by {self.doctor.user}"

# логи для действия пользователя
class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action} ({self.timestamp})"
