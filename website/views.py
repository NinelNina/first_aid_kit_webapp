from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Medicine
from .models import Firstaidkit


def home(request):
    first_aid_kit = Firstaidkit.objects.all()
    if request.user.is_authenticated:
        return render(request, 'home.html', {'first_aid_kit': first_aid_kit})
    else:
        return render(request, 'home.html', {})


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
    return render(request, 'medicine.html', {'medicine': medicine})


def firstaidkit_record(request, pk):
    if request.user.is_authenticated:
        firstaidkit_record = Firstaidkit.objects.get(id_firstaidkit=pk)
        return render(request, 'firstaikid_record.html', {'firstaidkit_record': firstaidkit_record})
    else:
        messages.success(request, "Страница доступна только для авторизованных пользователей.")
        return render(request, 'login.html', {})


def delete_firstaidkit_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Firstaidkit.objects.get(id_firstaidkit=pk)
        delete_it.delete()
        messages.success(request,"Запись успешно удалена.")
        return redirect('home')
    else:
        messages.success(request, "Страница доступна только для авторизованных пользователей.")
        return render(request, 'login.html', {})

def add_firstaidkit_record(request):
    return render(request, 'add_firstaidkit_record.html', {})