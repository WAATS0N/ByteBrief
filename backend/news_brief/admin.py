from django.contrib import admin
from .models import Publisher, Article, UserPreference

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active', 'created_at')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'country')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'category', 'published_at')
    list_filter = ('category', 'publisher')
    search_fields = ('title', 'summary')
    date_hierarchy = 'published_at'

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
