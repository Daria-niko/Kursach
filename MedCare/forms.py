from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'date_of_birth', 'login', 'password', 'role']

class MedicalStaffForm(forms.ModelForm):
    class Meta:
        model = MedicalStaff
        fields = ['user', 'phone_number']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'phone', 'address']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['medical_staff', 'document', 'academic_degree']


class MedicalCardForm(forms.ModelForm):
    snils_number = forms.CharField(max_length=14)
    insurance_policy_number = forms.CharField(max_length=20)
    patient = forms.ModelChoiceField(queryset=Patient.objects.all())  # Поле для пациента

    class Meta:
        model = MedicalCard
        fields = ['patient', 'snils_number', 'insurance_policy_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['snils_number'].initial = self.instance.snils_number
            self.fields['insurance_policy_number'].initial = self.instance.insurance_policy_number
            self.fields['patient'].initial = self.instance.patient

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Дополнительная логика обработки, если необходимо
        # Например, обработка зашифрованных данных
        # instance.snils_number = encrypt(self.cleaned_data['snils_number'])

        if commit:
            instance.save()  # Сохранение объекта без прямого присваивания значений защищенным атрибутам
        return instance

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'medical_card',
            'doctor',
            'date',
            'diagnosis',
            'prescription',
            'notes',
            'appointment_type',
            'record_status'
        ]

class AppointmentTypeForm(forms.ModelForm):
    class Meta:
        model = AppointmentType
        fields = ['name']

class RecordStatusForm(forms.ModelForm):
    class Meta:
        model = RecordStatus
        fields = ['name']


class MedicalRecordPatientForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['doctor', 'date']  # Пациент выбирает только врача и дату
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем врачей для выбора (например, только доступные)
        self.fields['doctor'].queryset = MedicalStaff.objects.all()

class UploadSQLForm(forms.Form):
    file = forms.FileField()

class UserSearchForm(forms.Form):
    last_name = forms.CharField(max_length=50, required=False, label='Фамилия')

class MedicalStaffSearchForm(forms.Form):
    last_name = forms.CharField(max_length=50, required=False, label='Фамилия')
    phone_number = forms.CharField(max_length=15, required=False, label='Телефон')

class MedicalRecordForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label="Пациент",
        empty_label="Выберите себя",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date = forms.DateField(
        label="Дата приема",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    doctor = forms.ModelChoiceField(
        queryset=MedicalStaff.objects.all(),
        label="Доктор",
        empty_label="Выберите доктора",
        widget=forms.Select(attrs={'class': 'form-select'})
    )