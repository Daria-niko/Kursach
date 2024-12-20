import csv
import os

from django.contrib.admin.models import LogEntry
from django.core.management  import call_command
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.shortcuts import get_object_or_404


from django.shortcuts import render
from django.utils.timezone import now

from .filters import MedicalRecordFilter
from .forms import *
from .utils import role_required


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(login=login)
                if password == user.password:
                    request.session['user_id'] = user.id
                    request.session['role'] = user.role.name

                    # Перенаправление в зависимости от роли
                    if user.role.name == 'Админ':
                        return redirect('admin_dashboard')
                    elif user.role.name == 'Пациент':
                        return redirect('patient_dashboard')
                    elif user.role.name == 'Доктор':
                        return redirect('doctor_dashboard')
                    else:
                        return redirect('login')
                else:
                    form.add_error(None, 'Неправильный пароль.')
            except User.DoesNotExist:
                form.add_error(None, 'Пользователь не найден.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@role_required('Админ')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@role_required('Пациент')
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

@role_required('Доктор')
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

# Список всех пользователей
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Создание нового пользователя
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

# Обновление существующего пользователя
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

# Удаление пользователя
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('user_list')


# Список всех сотрудников
def medical_staff_list(request):
    staff = MedicalStaff.objects.all()
    return render(request, 'medical_staff_list.html', {'staff': staff})

# Создание нового сотрудника
def medical_staff_create(request):
    if request.method == 'POST':
        form = MedicalStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_staff_list')
    else:
        form = MedicalStaffForm()
    return render(request, 'medical_staff_form.html', {'form': form})

# Обновление сотрудника
def medical_staff_update(request, pk):
    staff = get_object_or_404(MedicalStaff, pk=pk)
    if request.method == 'POST':
        form = MedicalStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('medical_staff_list')
    else:
        form = MedicalStaffForm(instance=staff)
    return render(request, 'medical_staff_form.html', {'form': form})

# Удаление сотрудника
def medical_staff_delete(request, pk):
    staff = get_object_or_404(MedicalStaff, pk=pk)
    staff.delete()
    return redirect('medical_staff_list')


# Список всех пациентов
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_listD(request):
    patients = Patient.objects.all()
    return render(request, 'patient_listForDoctor.html', {'patients': patients})

# Создание нового пациента
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})

# Обновление пациента
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form})

def patient_updateD(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_listForDoctor')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_formForD.html', {'form': form})

# Удаление пациента
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patient_list')


# Список образования
def education_list(request):
    education = Education.objects.all()
    return render(request, 'education_list.html', {'education': education})

# Создание нового образования
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationForm()
    return render(request, 'education_form.html', {'form': form})

# Обновление информации об образовании
def education_update(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationForm(instance=education)
    return render(request, 'education_form.html', {'form': form})

# Удаление информации об образовании
def education_delete(request, pk):
    education = get_object_or_404(Education, pk=pk)
    education.delete()
    return redirect('education_list')

# Список медицинских карт
def medical_card_list(request):
    medical_cards = MedicalCard.objects.all()
    return render(request, 'medical_card_list.html', {'medical_cards': medical_cards})

def medical_card_listD(request):
    medical_cards = MedicalCard.objects.all()
    return render(request, 'medical_card_listForDoctor.html', {'medical_cards': medical_cards})

# Создание медицинской карты
def medical_card_create(request):
    if request.method == 'POST':
        form = MedicalCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_card_list')
    else:
        form = MedicalCardForm()
    return render(request, 'medical_card_form.html', {'form': form})

# Обновление медицинской карты
def medical_card_update(request, pk):
    medical_card = get_object_or_404(MedicalCard, pk=pk)
    if request.method == 'POST':
        form = MedicalCardForm(request.POST, instance=medical_card)
        if form.is_valid():
            form.save()
            return redirect('medical_card_list')
    else:
        form = MedicalCardForm(instance=medical_card)
    return render(request, 'medical_card_form.html', {'form': form})

# Удаление медицинской карты
def medical_card_delete(request, pk):
    medical_card = get_object_or_404(MedicalCard, pk=pk)
    medical_card.delete()
    return redirect('medical_card_list')

# Список медицинских записей
def medical_record_list(request):
    medical_records = MedicalRecord.objects.all()

    # Фильтрация
    record_filter = MedicalRecordFilter(request.GET, queryset=medical_records)

    # Сортировка
    order_by = request.GET.get('sort', 'date')
    sorted_records = record_filter.qs.order_by(order_by)

    # Пагинация
    paginator = Paginator(sorted_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'medical_record_list.html',
        {'filter': record_filter, 'page_obj': page_obj, 'order_by': order_by}
    )

def medical_record_listForDoctor(request):
    medical_records = MedicalRecord.objects.all()

    # Фильтрация
    record_filter = MedicalRecordFilter(request.GET, queryset=medical_records)

    # Сортировка
    order_by = request.GET.get('sort', 'date')
    sorted_records = record_filter.qs.order_by(order_by)

    # Пагинация
    paginator = Paginator(sorted_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'medical_record_listForDoctor.html',
        {'filter': record_filter, 'page_obj': page_obj, 'order_by': order_by}
    )


# Создание медицинской записи
def medical_record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_record_form.html', {'form': form})

# Обновление медицинской записи
def medical_record_update(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm(instance=medical_record)
    return render(request, 'medical_record_form.html', {'form': form})

def medical_record_updateD(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            return redirect('medical_record_listForDoctor')
    else:
        form = MedicalRecordForm(instance=medical_record)
    return render(request, 'medical_record_formD.html', {'form': form})

# Удаление медицинской записи
def medical_record_delete(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    medical_record.delete()
    return redirect('medical_record_list')

def medical_record_deleteD(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    medical_record.delete()
    return redirect('medical_record_listForDoctor')

# Список типов приема
def appointment_type_list(request):
    appointment_types = AppointmentType.objects.all()
    return render(request, 'appointment_type_list.html', {'appointment_types': appointment_types})

# Создание нового типа приема
def appointment_type_create(request):
    if request.method == 'POST':
        form = AppointmentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_type_list')
    else:
        form = AppointmentTypeForm()
    return render(request, 'appointment_type_form.html', {'form': form})

# Обновление типа приема
def appointment_type_update(request, pk):
    appointment_type = get_object_or_404(AppointmentType, pk=pk)
    if request.method == 'POST':
        form = AppointmentTypeForm(request.POST, instance=appointment_type)
        if form.is_valid():
            form.save()
            return redirect('appointment_type_list')
    else:
        form = AppointmentTypeForm(instance=appointment_type)
    return render(request, 'appointment_type_form.html', {'form': form})

# Удаление типа приема
def appointment_type_delete(request, pk):
    appointment_type = get_object_or_404(AppointmentType, pk=pk)
    appointment_type.delete()
    return redirect('appointment_type_list')


# Список статусов записи
def record_status_list(request):
    record_statuses = RecordStatus.objects.all()
    return render(request, 'record_status_list.html', {'record_statuses': record_statuses})

# Создание нового статуса записи
def record_status_create(request):
    if request.method == 'POST':
        form = RecordStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_status_list')
    else:
        form = RecordStatusForm()
    return render(request, 'record_status_form.html', {'form': form})

# Обновление статуса записи
def record_status_update(request, pk):
    record_status = get_object_or_404(RecordStatus, pk=pk)
    if request.method == 'POST':
        form = RecordStatusForm(request.POST, instance=record_status)
        if form.is_valid():
            form.save()
            return redirect('record_status_list')
    else:
        form = RecordStatusForm(instance=record_status)
    return render(request, 'record_status_form.html', {'form': form})

# Удаление статуса записи
def record_status_delete(request, pk):
    record_status = get_object_or_404(RecordStatus, pk=pk)
    record_status.delete()
    return redirect('record_status_list')



def create_patient_record(request):
    patient = request.user  # получаем пациента
    medical_card = getattr(patient, 'medical_card', None)

    # Убедимся, что у пациента есть медицинская карта
    if not medical_card:
        return render(request, 'error.html', {'message': 'У вас нет медицинской карты'})

    if request.method == 'POST':
        form = MedicalRecordPatientForm(request.POST)
        if form.is_valid():
            # Получаем значения по умолчанию
            appointment_type = AppointmentType.objects.get(name="Плановый")
            record_status = RecordStatus.objects.get(name="Записан")

            # Создаём медицинскую запись
            MedicalRecord.objects.create(
                medical_card=medical_card,
                doctor=form.cleaned_data['doctor'],
                date=form.cleaned_data['date'],
                diagnosis="-",
                prescription="-",
                appointment_type=appointment_type,
                record_status=record_status,
            )
            return redirect('patient_dashboard')
    else:
        form = MedicalRecordPatientForm()

    return render(request, 'create_appointment.html', {'form': form})


def statistics_view(request):
    # Статистика: пациенты по годам
    patients_by_year = User.objects.filter(patient__isnull=False).annotate(
        year=ExtractYear('date_of_birth')
    ).values('year').annotate(count=Count('id'))

    # Статистика: записи по статусам
    records_by_status = MedicalRecord.objects.values('record_status__name').annotate(count=Count('id'))

    context = {
        'patients_by_year': patients_by_year,  # Передаем сам объект QuerySet
        'records_by_status': records_by_status,  # Передаем сам объект QuerySet
    }
    return render(request, 'statistics.html', context)


def export_users_to_csv(request):
    # Создаем HTTP-ответ с заголовками для скачивания файла CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # Создаем объект writer для записи в CSV
    writer = csv.writer(response)

    # Записываем заголовки столбцов в CSV
    writer.writerow(['ID', 'First Name', 'Last Name', 'Patronymic', 'Date of Birth', 'Login', 'Role'])

    # Записываем данные о пользователях
    users = User.objects.all()  # Получаем всех пользователей
    for user in users:
        writer.writerow(
            [user.id, user.first_name, user.last_name, user.patronymic, user.date_of_birth, user.login, user.role.name])

    return response

def backup_database(request):
    # Указываем путь для сохранения файла
    backup_dir = os.path.join("backups")
    os.makedirs(backup_dir, exist_ok=True)

    filename = f"backup_{now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(backup_dir, filename)

    with open(file_path, 'w') as backup_file:
        call_command('dumpdata', stdout=backup_file)

    # Возвращаем файл как ответ
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

from django.http import HttpResponse
from django.utils.html import escape
from .models import User, MedicalStaff
def export_sql(request):
    # Получаем данные о пользователях с ролью
    users = User.objects.select_related('role').all()

    # Проверка наличия данных
    if not users:
        return HttpResponse("Таблица пуста, ничего не для экспорта.")

    # Формируем SQL-скрипт вставки данных для User
    sql = 'INSERT INTO "User" (first_name, last_name, patronymic, date_of_birth, login, password, role_id) VALUES\n'

    try:
        sql += ",\n".join(
            [f"('{escape(str(user.first_name))}', '{escape(str(user.last_name))}', "
             f"'{escape(str(user.patronymic))}', '{escape(str(user.date_of_birth))}', "
             f"'{escape(str(user.login))}', '{escape(str(user.password))}', {user.role.id})"
             for user in users]
        )
    except IndexError:
        return HttpResponse("Ошибка индексации данных в запросе. Проверьте структуру таблицы.")

    sql += ";"

    # Получаем данные для медицинского персонала
    medical_staff = MedicalStaff.objects.all()

    # Формируем SQL-скрипт вставки данных для MedicalStaff
    sql += "\n\nINSERT INTO \"MedicalStaff\" (user_id, phone_number) VALUES\n"

    try:
        sql += ",\n".join(
            [f"({staff.user.id}, '{escape(str(staff.phone_number))}')"
             for staff in medical_staff]
        )
    except IndexError:
        return HttpResponse("Ошибка индексации данных в запросе. Проверьте структуру таблицы.")

    sql += ";"

    # Формируем ответ с SQL-данными
    response = HttpResponse(sql, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="export.sql"'
    return response

def import_users_from_csv(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']

        # Проверяем, является ли файл CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Неверный формат файла. Ожидается CSV.", status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Пропускаем заголовок
            next(reader, None)

            with transaction.atomic():
                for row in reader:
                    user_id, first_name, last_name, patronymic, date_of_birth, login, role_name = row

                    # Получаем или создаем роль
                    role, _ = Role.objects.get_or_create(name=role_name)

                    # Создаем или обновляем пользователя
                    User.objects.update_or_create(
                        id=user_id,
                        defaults={
                            'first_name': first_name,
                            'last_name': last_name,
                            'patronymic': patronymic,
                            'date_of_birth': date_of_birth,
                            'login': login,
                            'role': role
                        }
                    )

            return HttpResponse("Данные успешно импортированы из CSV.")
        except Exception as e:
            return HttpResponse(f"Ошибка при импорте CSV: {e}", status=500)

    return render(request, 'import_users.html')


from django.shortcuts import redirect

def import_data_from_sql(request):
    # Проверяем, был ли отправлен файл в запросе
    if request.method == 'POST' and request.FILES['sql_file']:
        sql_file = request.FILES['sql_file']

        # Проверяем, является ли файл SQL
        if not sql_file.name.endswith('.sql'):
            return HttpResponse("Неверный формат файла. Ожидается SQL.")

        # Читаем и выполняем SQL-скрипт
        try:
            sql_content = sql_file.read().decode('utf-8')

            with transaction.atomic():
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute(sql_content)

            # Редирект на страницу со списком пользователей после успешного выполнения
            return redirect('user_list')
        except Exception as e:
            return HttpResponse(f"Ошибка при выполнении SQL: {e}")

    return render(request, 'import_sql.html')


def user_logs(request):
    logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:100]
    return render(request, 'user_logs.html', {'logs': logs})


def user_list(request):
    form = UserSearchForm(request.GET)
    users = User.objects.all()

    if form.is_valid():
        last_name = form.cleaned_data.get('last_name')
        if last_name:
            users = users.filter(last_name__icontains=last_name)  # Фильтрация по фамилии

    return render(request, 'user_list.html', {'form': form, 'users': users})


def medical_staff_list(request):
    form = MedicalStaffSearchForm(request.GET)
    medical_staff = MedicalStaff.objects.all()

    if form.is_valid():
        last_name = form.cleaned_data.get('last_name')
        phone_number = form.cleaned_data.get('phone_number')

        if last_name:
            medical_staff = medical_staff.filter(user__last_name__icontains=last_name)

        if phone_number:
            medical_staff = medical_staff.filter(phone_number__icontains=phone_number)

    return render(request, 'medical_staff_list.html', {'form': form, 'medical_staff': medical_staff})


def statistics_view(request):
    # Получаем количество записей по статусам
    records_by_status = MedicalRecord.objects.values('record_status__name').annotate(count=Count('id'))

    # Подсчитываем общее количество записей для вычисления процента
    total_records = MedicalRecord.objects.count()

    # Получаем количество пользователей по ролям
    users_by_role = User.objects.values('role__name').annotate(count=Count('id'))

    return render(request, 'statistics.html', {
        'records_by_status': records_by_status,
        'total_records': total_records,
        'users_by_role': users_by_role,
    })

def patient_list(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос из GET-параметра
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(user__last_name__icontains=query)  # Фильтруем только по фамилии

    return render(request, 'patient_list.html', {'patients': patients})

def patient_list(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос из GET-параметра
    patients = Patient.objects.all()

    if query:
        # Фильтруем пациентов по фамилии
        patients = patients.filter(user__last_name__icontains=query)

    return render(request, 'patient_list.html', {'patients': patients})

def patient_listD(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос из GET-параметра
    patients = Patient.objects.all()

    if query:
        # Фильтруем пациентов по фамилии
        patients = patients.filter(user__last_name__icontains=query)

    return render(request, 'patient_listForDoctor.html', {'patients': patients})

def create_medical_recordP(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            patient = form.cleaned_data['patient']
            doctor = form.cleaned_data['doctor']
            date = form.cleaned_data['date']

            # Получаем первые записи для AppointmentType и RecordStatus
            default_appointment_type = AppointmentType.objects.first()
            default_record_status = RecordStatus.objects.first()

            # Создаем медицинскую запись с дефолтными значениями для Diagnosis, Prescription и Notes
            MedicalRecord.objects.create(
                medical_card=patient.medical_card,
                doctor=doctor,
                date=date,
                diagnosis="-",
                prescription="-",
                notes="-",
                appointment_type=default_appointment_type,
                record_status=default_record_status
            )
            return redirect('patient_dashboard')  # Перенаправление на список записей или другую страницу
    else:
        form = MedicalRecordForm()

    return render(request, 'create_medical_recordP.html', {'form': form})

