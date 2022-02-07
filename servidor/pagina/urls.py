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
    path('mark_and_model/<int:marcaModelo_actual>/<int:tipo_carga>/<int:redirigir>', views.mark_and_model, name='mark_and_model'),
    path('informes', views.informes, name='informes'),
    path('factura', views.factura, name='factura'),
    path('compra', views.compra, name='compra'),
    path('historial_compra', views.historial_compra, name='historial_compra'),
    path('factura_compra', views.factura_comprar, name='factura_compra'),
    path('cash', views.cash, name='cash'),
    path('cash_history', views.cash_history, name='cash_history'),
    path('cash_register', views.cash_register, name='cash_register'),
    path('cash_detail_delete/<int:detalle_caja_actual>', views.cash_detail_delete, name='cash_detail_delete'),
    path('modal_view_cash/<int:caja_actual>', views.modal_view_cash, name='modal_view_cash'),
    path('close_cash_register/<int:id_caja_actual>', views.close_cash_register, name='close_cash_register'),
    path('cancelar_pagare', views.cancelar_pagare, name='cancelar_pagare'),
    path('personas', views.personas, name='personas'),
    path('clientes/<int:mode>', views.clientes, name='clientes'),
    path('proveedores/<int:mode>', views.proveedores, name='proveedores'),
    path('edit_proveedor/<int:proveedor_actual>', views.edit_proveedor, name='edit_proveedor'),
    path('modal_proveedor/<int:proveedor_actual>', views.edit_proveedor, name='modal_proveedor'),
    path('modal_view_proveedor', views.modal_view_proveedor, name='modal_view_proveedor'),
    path('timbrado/<int:proveedor_actual>', views.timbrados, name='timbrado'),
    path('delete_timbrado/<int:timbra_actual>', views.delete_timbrado, name='delete_timbrado'),
    path('edit_client/<int:clie_actual>', views.edit_client, name="edit_client"),
    path('config', views.config, name='config'),
    path('parameters_products', views.parameters_products, name='parameters_products'),
    path('mark', views.mark, name='mark'),
    path('edit_mark/<int:mark_actual>', views.edit_mark, name='edit_mark'),
    path('edit_color/<int:color_actual>', views.edit_color, name='edit_color'),
    path('models', views.models, name='models'),
    path('color', views.colors, name='color'),
    path('parameters_clients', views.parameters_clients, name='parameters_clients'),
    path('document', views.document, name='document'),
    path('country', views.country, name='country'),
    path('delete_country/<int:country_actual>', views.delete_country, name='delete_country'),
    path('city', views.city, name='city'),
    path('delete_city/<int:city_actual>', views.delete_city, name='delete_city'),
    path('edit_document/<int:document_actual>/<int:tipo_carga>', views.parameters_modal_client, name='edit_document'),
    path('delete_document/<int:document_actual>', views.delete_document, name='delete_document'),
    path('delete_color/<int:color_actual>', views.delete_color, name='delete_color'),
    path('delete_model/<int:model_actual>', views.delete_model, name='delete_model'),
    path('delete_mark/<int:mark_actual>', views.delete_mark, name='delete_mark'),
    path('users', views.users, name='users'),
    path('edit_user/<int:usu_actual>', views.edit_user, name='edit_user'),
    path('delete_user/<int:usu_actual>', views.delete_user, name='delete_user'),
    path('parameters_modal_client/<int:paisCiudad_actual>/<int:tipo_carga>/<int:redirigir>', views.parameters_modal_client, name='parameters_modal_client'),
    path('disable_client/<int:clie_actual>/<int:option>', views.disable_client, name='disable_client'),
    path('disable_proveedor/<int:proveedor_actual>/<int:option>', views.disable_proveedor, name='disable_proveedor'),
]