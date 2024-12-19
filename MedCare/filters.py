# filters.py
import django_filters

from .models import MedicalRecord

class MedicalRecordFilter(django_filters.FilterSet):
    medical_card__patient__user__last_name = django_filters.CharFilter(
        field_name='medical_card__patient__user__last_name', lookup_expr='icontains', label='Фамилия пациента'
    )
    doctor__user__last_name = django_filters.CharFilter(
        field_name='doctor__user__last_name', lookup_expr='icontains', label='Фамилия доктора'
    )
    diagnosis = django_filters.CharFilter(
        lookup_expr='icontains', label='Диагноз'
    )
    date = django_filters.DateFromToRangeFilter(
        label='Дата записи (от - до)'
    )

    class Meta:
        model = MedicalRecord
        fields = ['medical_card__patient__user__last_name', 'doctor__user__last_name', 'diagnosis', 'date']
