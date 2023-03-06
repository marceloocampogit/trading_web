from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_view, register, user_list, user_profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name = 'users/login.html'), name='logout'),
    path('register/', register, name='register'),
    path('list/', user_list, name='user_list'),
    path('profile/', user_profile, name='profile')
]