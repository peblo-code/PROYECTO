from django.urls import path
from pagina import views

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('', views.login, name='login'),
    path('salir', views.salir, name='salir'),
    path('productos', views.productos, name='productos'),
    path('edit_product/<int:product_actual>', views.edit_product, name="edit_product"),
    path('modal_info/<int:product_actual>', views.modal_info, name='modal_info'),
    path('delete_product/<int:product_actual>', views.delete_product, name='delete_product'),
    path('mark_and_model/<int:marcaModelo_actual>/<int:tipo_carga>', views.mark_and_model, name='mark_and_model'),
    path('informes', views.informes, name='informes'),
    path('factura', views.factura, name='factura'),
    path('cancelar_pagare', views.cancelar_pagare, name='cancelar_pagare'),
    path('clientes', views.clientes, name='clientes'),
    path('edit_client/<int:clie_actual>', views.edit_client, name="edit_client"),
    path('config', views.config, name='config'),
    path('users', views.users, name='users'),
    path('edit_user/<int:usu_actual>', views.edit_user, name='edit_user'),
    path('delete_user/<int:usu_actual>', views.delete_user, name='delete_user'),
    path('parameters_modal_client/<int:paisCiudad_actual>/<int:tipo_carga>', views.parameters_modal_client, name='parameters_modal_client'),
    path('disable_client/<int:clie_actual>/<int:option>', views.disable_client, name='disable_client'),
]