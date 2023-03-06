from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from users.forms import RegisterForm

# Create your views here.

def login_view(request):
    #Si voy por get, le muestro el formulario
    if request.method == 'GET':
        return render(request, 'users/login.html')

    #Si voy por post, valido el formulario
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #Si el formulario es válido, se autentica el usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            #Si el usuario existe, se loguea
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            #Si el formulario no es válido, se vuelve a mostrar
            context = {
                'errors': form.errors,
            }
            return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #Creo objeto usuario
            form.save()
            return redirect('login')
        else:
            context = {
                'errors': form.errors,
            }
            return render(request, 'users/register.html', context)

def user_list(request):
    return render(request, 'users/user_list.html')

def user_profile(request):
    return render(request, 'users/profile.html')