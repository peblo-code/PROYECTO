from django.urls import path
from django.urls.resolvers import URLPattern

urlpatterns = [
    path('', views.inicio, name='inicio'),
]