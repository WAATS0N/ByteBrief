from django.urls import path
from . import views

urlpatterns = [

    path('api/generate-digest/', views.generate_digest_api, name='generate_digest_api'),
    path('api/metadata/', views.get_metadata, name='get_metadata'),
]
