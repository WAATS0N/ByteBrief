"""
URL configuration for bytebrief_web project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_brief.urls')),
]
