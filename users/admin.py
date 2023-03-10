from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'profile_picture', 'cover_image', 'occupation',\
    'description', 'availability', 'birth_date', 'years_of_experience',\
    'address', 'company_name', 'language', 'country')