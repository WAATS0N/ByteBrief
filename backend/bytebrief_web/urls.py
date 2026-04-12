"""
URL configuration for bytebrief_web project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from news_brief import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # News Brief API
    path('', include('news_brief.urls')),

    # Auth API (JWT)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/google/', views.GoogleLoginView.as_view(), name='google_login'),

    # Required for dj-rest-auth password reset email to build the URL
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),

    # Allauth (handles Google OAuth redirect flow at /accounts/google/login/)
    path('accounts/', include('allauth.urls')),

    # ── React Router Catch-All ──────────────────────────────────────────────────
    # Serve index.html for all non-API, non-admin, non-static routes so that
    # React Router can handle client-side navigation (direct links, refresh, etc.)
    re_path(r'^(?!api/|admin/|accounts/|static/).*$',
            TemplateView.as_view(template_name='index.html'),
            name='react_router_catchall'),
]
