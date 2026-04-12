"""
URL configuration for bytebrief_web project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from news_brief import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health Check
    path('ping/', views.ping, name='ping'),

    # News Brief API (now prefixed at the root for clarity)
    path('api/', include('news_brief.urls')),

    # Auth API (JWT)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/google/', views.GoogleLoginView.as_view(), name='google_login'),

    # Required for dj-rest-auth password reset email to build the URL
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),

    # Allauth (handles Google OAuth redirect flow at /accounts/google/login/)
    path('accounts/', include('allauth.urls')),

    # ── React Router Catch-All ──────────────────────────────────────────────────
    # Using a custom view (serve_react) instead of TemplateView for better
    # robustness and diagnostic logging in production.
    re_path(r'^(?!api/|admin/|accounts/|static/|ping/).*$',
            views.serve_react,
            name='react_router_catchall'),
]

