"""
URL configuration for bytebrief_web project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_brief.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
