from django.contrib import admin
from .models import Publisher, Article, UserPreference, Bookmark, SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'subject', 'message')
    readonly_fields = ('user', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


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

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')
