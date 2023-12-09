from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from .forms import SignUpForm, AddFirstAidKitRecord, DiseaseSearchForm
from .models import Medicine, MedicationUse, Disease, DiseaseCatalog, Symptom
from .models import Firstaidkit

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    if request.user.is_authenticated:
        return redirect('firstaidkit')
    else:
        return render(request, 'home.html', {})


def medicine_list(request):
    medications = Medicine.objects.select_related().all().order_by('medicine_name')
    data = []

    for medication in medications:
        medication_uses = MedicationUse.objects.filter(id_medicine=medication.id_medicine)
        diseases = medication_uses.values('id_disease', 'id_disease__disease_name')

        data.append({
            'medication': medication,
            'diseases': diseases
        })

    objects_at_page = 20
    paginator = Paginator(data, objects_at_page)

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'medicine_list.html', {'data': data, 'medicine_count': medications.count()})


def firstaidkit(request):
    if request.user.is_authenticated:
        first_aid_kit = Firstaidkit.objects.filter(user_id=request.user.id)

        current_date = timezone.now().date()
        for record in first_aid_kit:
            record.is_expired = record.expiration_date.year <= current_date.year and record.expiration_date.month <= current_date.month

        objects_at_page = 20
        if len(first_aid_kit) > objects_at_page:
            paginator = Paginator(first_aid_kit, objects_at_page)
            page = request.GET.get('page')
            try:
                first_aid_kit = paginator.page(page)
            except PageNotAnInteger:
                first_aid_kit = paginator.page(1)
            except EmptyPage:
                first_aid_kit = paginator.page(paginator.num_pages)
        return render(request, 'firstaidkit.html', {'first_aid_kit': first_aid_kit})
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return render(request, 'login.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли!")
            return redirect('home')
        else:
            messages.success(request, "Ошибка входа, пожалуйста, попробуйте ещё раз.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Вы вышли.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def medicine_description(request, pk):
    medicine = Medicine.objects.get(id_medicine=pk)
    medication_use = MedicationUse.objects.filter(id_medicine=pk).order_by('id_disease__id_disease')
    diseases = medication_use.values('id_disease', 'id_disease__disease_name')

    previous_url = request.META.get('HTTP_REFERER', reverse('home'))
    return render(request, 'medicine.html', {'medicine': medicine, 'diseases': diseases, 'previous_url': previous_url})


def disease_description(request, pk):
    disease = Disease.objects.get(id_disease=pk)
    medications = MedicationUse.objects.filter(id_disease=pk)
    medications = medications.values('id_medicine', 'id_medicine__medicine_name').order_by('id_medicine__medicine_name')
    symptoms = DiseaseCatalog.objects.filter(id_disease=pk).order_by('id_symptom__symptom_name')
    symptoms = symptoms.values('id_disease', 'id_symptom__symptom_name')

    previous_url = request.META.get('HTTP_REFERER', reverse('home'))
    return render(request, 'disease.html',
                  {'disease': disease, 'medications': medications, 'symptoms': symptoms, 'previous_url': previous_url})


def delete_firstaidkit_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Firstaidkit.objects.get(id_firstaidkit=pk)
        delete_it.delete()
        messages.success(request, "Запись успешно удалена.")
        return redirect('firstaidkit')
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return render(request, 'login.html', {})


def add_firstaidkit_record(request):
    if request.user.is_authenticated:
        form = AddFirstAidKitRecord(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                add_firstaidkit_record = form.save(commit=False)
                add_firstaidkit_record.user_id = request.user.id
                add_firstaidkit_record = form.save()
                messages.success(request, "Запись добавлена.")
                return redirect('firstaidkit')
        return render(request, 'add_firstaidkit_record.html', {'form': form})
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return redirect('login')


def update_firstaidkit_record(request, pk):
    if request.user.is_authenticated:
        current_record = Firstaidkit.objects.get(id_firstaidkit=pk)
        form = AddFirstAidKitRecord(instance=current_record)
        if request.method == 'POST':
            form = AddFirstAidKitRecord(request.POST, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Запись обновлена.")
                return redirect('firstaidkit')
        return render(request, 'update_firstaidkit_record.html', {'form': form})
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return redirect('login')


def diseases_list(request):
    diseases = Disease.objects.select_related().all().order_by('id_disease')
    data = []

    for disease in diseases:
        medication_uses = MedicationUse.objects.filter(id_disease=disease.id_disease)
        medications = medication_uses.values('id_medicine', 'id_medicine__medicine_name').order_by(
            'id_medicine__medicine_name')

        data.append({
            'disease': disease,
            'medications': medications
        })

    objects_at_page = 20
    paginator = Paginator(data, objects_at_page)

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'disease_list.html', {'data': data, 'diseases_count': diseases.count()})


def symptoms_list(request):
    symptoms = Symptom.objects.select_related().all().order_by('symptom_name')
    data = []

    for symptom in symptoms:
        disease_catalog = DiseaseCatalog.objects.filter(id_symptom=symptom.id_symptom)
        diseases = disease_catalog.values('id_disease', 'id_disease__disease_name').order_by('id_disease')

        data.append({
            'symptom': symptom,
            'diseases': diseases
        })

    objects_at_page = 20
    paginator = Paginator(data, objects_at_page)

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'symptom_list.html', {'data': data})


def search_medicine(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        if searched or str(searched) != '':
            data = Medicine.objects.filter(medicine_name__icontains=searched).order_by('medicine_name')
            objects_at_page = 20
            if len(data) > objects_at_page:
                paginator = Paginator(data, objects_at_page)
                page = request.GET.get('page')
                try:
                    data = paginator.page(page)
                except PageNotAnInteger:
                    data = paginator.page(1)
                except EmptyPage:
                    data = paginator.page(paginator.num_pages)
            return render(request, 'search_medicine.html', {'searched': searched, 'data': data})
    else:
        return redirect('medicine_list')


def search_disease(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        if searched or str(searched) != '':
            data = Disease.objects.filter(disease_name__icontains=searched).order_by('id_disease')
            objects_at_page = 20
            if len(data) > objects_at_page:
                paginator = Paginator(data, objects_at_page)
                page = request.GET.get('page')
                try:
                    data = paginator.page(page)
                except PageNotAnInteger:
                    data = paginator.page(1)
                except EmptyPage:
                    data = paginator.page(paginator.num_pages)
            return render(request, 'search_disease.html', {'searched': searched, 'data': data})
    else:
        return redirect('diseases_list')


def search_firstaidkit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched']
            if searched or str(searched) != '':
                first_aid_kit = Firstaidkit.objects.filter(user_id=request.user.id)
                disease_ids = MedicationUse.objects.filter(id_disease__disease_name__icontains=searched).values_list(
                    'id_disease', flat=True).distinct()
                diseases = Disease.objects.filter(id_disease__in=disease_ids)
                medication_use_ids = MedicationUse.objects.filter(
                    id_disease__disease_name__icontains=searched).values_list('id_medicine', flat=True)
                data = first_aid_kit.filter(id_medicine__in=medication_use_ids)

                current_date = timezone.now().date()
                for record in data:
                    record.is_expired = record.expiration_date.year <= current_date.year and record.expiration_date.month <= current_date.month

                objects_at_page = 20
                if len(data) > objects_at_page:
                    paginator = Paginator(data, objects_at_page)
                    page = request.GET.get('page')
                    try:
                        data = paginator.page(page)
                    except PageNotAnInteger:
                        data = paginator.page(1)
                    except EmptyPage:
                        data = paginator.page(paginator.num_pages)
                return render(request, 'search_firstaidkit.html',
                              {'searched': searched, 'data': data, 'diseases': diseases})
        else:
            return redirect('firstaidkit')
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return redirect('login')


def search_disease_by_symptom(request):
    form = DiseaseSearchForm()

    if request.method == 'POST':
        form = DiseaseSearchForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']

            q_objects = Q()
            for symptom in symptoms:
                q_objects &= Q(
                    id_disease__in=DiseaseCatalog.objects.filter(id_symptom=symptom).values_list('id_disease',
                                                                                                 flat=True))

            diseases = Disease.objects.filter(q_objects)

            return render(request, 'search_disease_by_symptom.html',
                          {'diseases': diseases, 'selected_symptoms': symptoms, 'form': form})

    return render(request, 'search_disease_by_symptom.html', {'form': form})
