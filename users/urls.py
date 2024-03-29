from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_view, register, user_list, user_profile, block_user_view, delete_user_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name = 'users/login.html'), name='logout'),
    path('register/', register, name='register'),
    
    path('user-list/', user_list, name='user_list'),
    path('profile/', user_profile, name='profile'),

    path('block/<int:pk>/', block_user_view, name='block'),
    path('delete/<int:pk>/', delete_user_view, name='delete')

]