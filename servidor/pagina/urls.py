from django.urls import path
from pagina import views

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('', views.login, name='login'),
    path('salir', views.salir, name='salir'),
]