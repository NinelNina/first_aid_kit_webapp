from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from .forms import SignUpForm, AddFirstAidKitRecord
from .models import Medicine
from .models import Firstaidkit


def home(request):
    # if request.user.is_authenticated:
    #     first_aid_kit = Firstaidkit.objects.filter(user_id=request.user.id)
    #     return render(request, 'home.html', {'first_aid_kit': first_aid_kit})
    # else:
    return render(request, 'home.html', {})


def firstaidkit(request):
    if request.user.is_authenticated:
        first_aid_kit = Firstaidkit.objects.filter(user_id=request.user.id)
        return render(request, 'firstaikit.html', {'first_aid_kit': first_aid_kit})
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
    messages.success(request,"Вы вышли.")
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
    previous_url = request.META.get('HTTP_REFERER', reverse('home'))
    return render(request, 'medicine.html', {'medicine': medicine, 'previous_url': previous_url})


def delete_firstaidkit_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Firstaidkit.objects.get(id_firstaidkit=pk)
        delete_it.delete()
        messages.success(request,"Запись успешно удалена.")
        return redirect('firstaidkit')
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return render(request, 'login.html', {})


def add_firstaidkit_record(request):
    form = AddFirstAidKitRecord(request.POST or None)
    if request.user.is_authenticated:
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
        form = AddFirstAidKitRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена.")
            return redirect('firstaidkit')
        return render(request, 'update_firstaidkit_record.html', {'form': form})
    else:
        messages.success(request, "Страница доступна только авторизованным пользователям.")
        return redirect('login')