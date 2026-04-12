from django.urls import path
from . import views
from .account_views import (
    UserProfileView, DeleteAccountView, UserSettingsView,
    ReadingHistoryView, NotificationView, SupportTicketView
)

urlpatterns = [
    path('generate-digest/', views.generate_digest_api, name='generate_digest_api'),
    path('metadata/', views.get_metadata, name='get_metadata'),
    path('admin/force-scrape/', views.force_scrape_api, name='force_scrape_api'),
    path('admin/clear-users/', views.clear_users_api, name='clear_users_api'),

    # Account Settings
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('user/preferences/', views.user_preferences_api, name='user_preferences'),
    path('user/settings/', UserSettingsView.as_view(), name='user_settings'),
    path('user/bookmarks/', views.user_bookmarks_api, name='user_bookmarks'),
    path('user/history/', ReadingHistoryView.as_view(), name='user_history'),
    path('user/notifications/', NotificationView.as_view(), name='user_notifications'),
    path('api/support/ticket/', SupportTicketView.as_view(), name='support_ticket'), # kept api/ prefix for consistency with existing calls if any
]

