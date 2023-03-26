from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models.signals import post_save
from django.dispatch import receiver

from admin_settings.models import Country, Language
from users.forms import RegisterForm, UserProfileForm
from users.models import UserProfile

from news.utils import get_random_news

# Create your views here.
@login_required
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

@login_required
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

@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect('index')

    context = {
        'users': User.objects.exclude(id=request.user.id),
    }

    return render(request, 'users/user_list.html', context=context)

@login_required
def user_profile(request):
    if request.method == 'GET':
        #Separo la noticia principal de las secundarias
        main_new, other_news = get_random_news()
        context = {
            #Paso por contexto lenguajes y paises para mostrar en el front
            'languages': Language.objects.all(),
            'countries': Country.objects.all(),
            'main_new': main_new,
            'other_news': other_news,
        }
        return render(request, 'users/profile.html', context = context)\
    
    elif request.method == 'POST':

        data = request.POST.copy()

        #Si me llega un country y ese country existe, guardo el objeto country
        if request.POST.get('country') and Country.objects.filter(name = request.POST.get('country')).exists():
            country = Country.objects.get(name = request.POST.get('country'))
            #Hago esto porque al request le llega un string y precisa una FK para validar contra country
            data['country'] = country.id

        #Si me llega un language y ese language existe, guardo el objeto language
        if request.POST.get('language') and Language.objects.filter(name = request.POST.get('language')).exists():
            language = Language.objects.get(name = request.POST.get('language'))
            #Hago esto porque al request le llega un string y precisa una FK para validar contra languages
            data['language'] = language.id

        #En vez de pasarle request.POST, le mando la data editada
        form = UserProfileForm(data, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@login_required
def block_user_view(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    user = User.objects.get(id=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')

@login_required
def delete_user_view(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    User.objects.get(id=pk).delete()
    return redirect('user_list')