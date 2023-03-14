from django.contrib import admin

from news.models import News
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url_to_news', 'url_to_image', 'published_at')