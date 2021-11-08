from django.urls import path
from pagina import views

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('', views.login, name='login'),
    path('salir', views.salir, name='salir'),
    path('productos', views.productos, name='productos'),
    path('busqueda_producto', views.busqueda_producto, name="busqueda_producto"),
    path('informes', views.informes, name='informes'),
    path('factura', views.factura, name='factura'),
    path('cancelar_pagare', views.cancelar_pagare, name='cancelar_pagare'),
    path('nuevo_cliente', views.nuevo_cliente, name='nuevo_cliente'),
]