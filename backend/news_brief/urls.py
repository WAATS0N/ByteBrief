from django.urls import path
from . import views
from .account_views import (
    UserProfileView, DeleteAccountView, UserSettingsView,
    ReadingHistoryView, NotificationView, SupportTicketView
)

urlpatterns = [
    path('api/generate-digest/', views.generate_digest_api, name='generate_digest_api'),
    path('api/metadata/', views.get_metadata, name='get_metadata'),

    # Account Settings
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/user/delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('api/user/preferences/', views.user_preferences_api, name='user_preferences'),
    path('api/user/settings/', UserSettingsView.as_view(), name='user_settings'),
    path('api/user/bookmarks/', views.user_bookmarks_api, name='user_bookmarks'),
    path('api/user/history/', ReadingHistoryView.as_view(), name='user_history'),
    path('api/user/notifications/', NotificationView.as_view(), name='user_notifications'),
    path('api/support/ticket/', SupportTicketView.as_view(), name='support_ticket'),
]
