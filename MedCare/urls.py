
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),

    # Пользователи
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    # Сотрудники
    path('medical_staff/', views.medical_staff_list, name='medical_staff_list'),
    path('medical_staff/create/', views.medical_staff_create, name='medical_staff_create'),
    path('medical_staff/update/<int:pk>/', views.medical_staff_update, name='medical_staff_update'),
    path('medical_staff/delete/<int:pk>/', views.medical_staff_delete, name='medical_staff_delete'),

    # Пациенты
    path('patients/', views.patient_list, name='patient_list'),
    path('patientsD/', views.patient_listD, name='patient_listD'),
    path('patient_listForDoctor/', views.patient_listD, name='patient_listForDoctor'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/update/<int:pk>/', views.patient_update, name='patient_update'),
    path('patients/updateD/<int:pk>/', views.patient_updateD, name='patient_updateD'),
    path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),

# Образование
    path('education/', views.education_list, name='education_list'),
    path('education/create/', views.education_create, name='education_create'),
    path('education/update/<int:pk>/', views.education_update, name='education_update'),
    path('education/delete/<int:pk>/', views.education_delete, name='education_delete'),

    # Медицинские карты
    path('medical_cards/', views.medical_card_list, name='medical_card_list'),
    path('medical_card_listForDoctor/', views.medical_card_listD, name='medical_card_listForDoctor'),
    path('medical_cards/create/', views.medical_card_create, name='medical_card_create'),
    path('medical_cards/update/<int:pk>/', views.medical_card_update, name='medical_card_update'),
    path('medical_cards/delete/<int:pk>/', views.medical_card_delete, name='medical_card_delete'),

# Медицинские записи
    path('medical_records/', views.medical_record_list, name='medical_record_list'),
    path('medical_record_listForDoctor/', views.medical_record_listForDoctor, name='medical_record_listForDoctor'),
    path('medical_records/create/', views.medical_record_create, name='medical_record_create'),
    path('medical_records/update/<int:pk>/', views.medical_record_update, name='medical_record_update'),
    path('medical_recordsD/update/<int:pk>/', views.medical_record_updateD, name='medical_record_updateD'),
    path('medical_records/delete/<int:pk>/', views.medical_record_delete, name='medical_record_delete'),
    path('medical_recordsD/delete/<int:pk>/', views.medical_record_deleteD, name='medical_record_deleteD'),

    # Типы приема
    path('appointment_types/', views.appointment_type_list, name='appointment_type_list'),
    path('appointment_types/create/', views.appointment_type_create, name='appointment_type_create'),
    path('appointment_types/update/<int:pk>/', views.appointment_type_update, name='appointment_type_update'),
    path('appointment_types/delete/<int:pk>/', views.appointment_type_delete, name='appointment_type_delete'),

# Статусы записи
    path('record_statuses/', views.record_status_list, name='record_status_list'),
    path('record_statuses/create/', views.record_status_create, name='record_status_create'),
    path('record_statuses/update/<int:pk>/', views.record_status_update, name='record_status_update'),
    path('record_statuses/delete/<int:pk>/', views.record_status_delete, name='record_status_delete'),

    path('statistics/', views.statistics_view, name='statistics'),

    path('patient/create-record/', views.create_patient_record, name='create_patient_record'),

    path('backup/', views.backup_database, name='backup_database'),
    path('export_users/', views.export_users_to_csv, name='export_users'),

    path('export_sql/', views.export_sql, name='export_sql'),

    path('import_csv/', views.import_users_from_csv, name='import_csv'),
    path('import/sql/', views.import_data_from_sql, name='import_sql'),

    path('user-logs/', views.user_logs, name='user_logs'),

    path('create_medical_recordP/', views.create_medical_recordP, name='create_medical_recordP'),
]