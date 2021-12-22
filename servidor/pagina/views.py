from django.shortcuts import redirect, render
from pagina.models import usuarios
from pagina.models import tipo_usuario
from pagina.models import vehiculo
from pagina.models import marca
from pagina.models import modelo
from pagina.models import color
from pagina.models import tipo_documento
from pagina.models import pais
from pagina.models import ciudad
from pagina.models import cliente

# Create your views here.
def validar(request, pageSuccess, parameters={}):
    if request.session.get("id_usuario"):
        if (request.session.get("tipo_usuario") == 2) and (pageSuccess == 'sections/config.html'):
            return render(request, "index.html", {"nombre_completo": request.session.get("nombre_completo"), "mensaje": "Este usuario no cuenta con los privilegios suficientes"})
        else: 
            return render(request, pageSuccess, {"nombre_completo": request.session.get("nombre_completo"),"parameters": parameters})
    else:
        return render(request, 'login.html')


def login(request):
    if request.method == 'GET':
        if request.session.get("id_usuario"):
            return redirect("inicio")
        else:
            return render(request, 'login.html')

    if request.method == 'POST':
        v_usuario = request.POST.get("usuario")
        v_clave = request.POST.get("clave")
        usuario_actual = usuarios.objects.filter(usuario=v_usuario).exists()
        if usuario_actual:
            datos_usuario=usuarios.objects.filter(usuario=v_usuario).first()
            if getattr(datos_usuario, "clave") == v_clave:
                request.session["id_usuario"]=getattr(datos_usuario, "id_usuario")
                request.session["nombre_completo"]=getattr(datos_usuario, "nombre_completo")
                request.session["tipo_usuario"]=getattr(datos_usuario, "tipo_usuario")
                return redirect("inicio")
            else:
                return render(request, 'login.html', {"mensaje": "Por favor, vuelva a intentarlo!"})
        else:
            return render(request, 'login.html', {"mensaje": "Por favor, vuelva a intentarlo!"})

def inicio(request):
    usu_actual = request.session.get("id_usuario")
    datos_usuario=usuarios.objects.filter(id_usuario=usu_actual).first()
    return validar(request, 'index.html', {"datos_usuario": datos_usuario})

def header(request):
    return render(request, 'header.html')

def salir(request):
    request.session.flush()
    return redirect("./")

def productos(request):
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    return validar(request, 'sections/products/products.html',{"listaproducto":listaproducto, "listamarca":listamarca, 
    "listamodelo": listamodelo, "listacolor":listacolor})

def edit_product(request, product_actual = 0):
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    if request.method=="GET":
        vehiculo_actual=vehiculo.objects.filter(id_vehiculo=product_actual).exists()
        if vehiculo_actual:
            datos_vehiculo=vehiculo.objects.filter(id_vehiculo=product_actual).first()
            return validar(request, 'sections/products/modal_product.html',
            {"datos_act":datos_vehiculo, "product_actual":product_actual, "titulo":"Editar un Producto", 
            "listamarca":listamarca, "listamodelo": listamodelo, "listacolor":listacolor})
        else:
            return validar(request, "sections/products/edit_product.html", {"titulo":"Cargar nuevo Producto",
            "listamarca":listamarca, "listamodelo": listamodelo, "listacolor": listacolor, "product_actual": product_actual})

    if request.method=="POST":
        if product_actual==0:
            vehiculo_nuevo=vehiculo(id_marca_id=request.POST.get('marca'),
            id_modelo_id=request.POST.get('modelo'), 
            id_color_id=request.POST.get("color"),
            transmision_vehiculo=request.POST.get("transmision"),
            motor_vehiculo=request.POST.get("motor"),
            anio_vehiculo=request.POST.get("anio"),
            nro_chassis_vehiculo=request.POST.get("chasis"),
            precio_costo=request.POST.get("costo"),
            precio_venta=request.POST.get("venta"),
            estado_vehiculo=request.POST.get("existencia"))
            vehiculo_nuevo.save()
        else:
            vehiculo_actual=vehiculo.objects.get(id_vehiculo=product_actual)
            vehiculo_actual.id_marca_id=request.POST.get("marca")
            vehiculo_actual.id_modelo_id=request.POST.get("modelo")
            vehiculo_actual.id_color_id=request.POST.get("color")
            vehiculo_actual.transmision_vehiculo=request.POST.get("transmision")
            vehiculo_actual.motor_vehiculo=request.POST.get("motor")
            vehiculo_actual.anio_vehiculo=request.POST.get("anio")
            vehiculo_actual.nro_chassis_vehiculo=request.POST.get("chasis")
            vehiculo_actual.precio_costo=request.POST.get("costo")
            vehiculo_actual.precio_venta=request.POST.get("venta")
            vehiculo_actual.estado_vehiculo=request.POST.get("existencia")
            vehiculo_actual.save()
        
        return redirect("../productos")

def modal_info(request, product_actual):
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    if request.method=="GET":
        vehiculo_actual=vehiculo.objects.filter(id_vehiculo=product_actual).exists()
        if vehiculo_actual:
            datos_vehiculo=vehiculo.objects.filter(id_vehiculo=product_actual).first()
            return validar(request, 'sections/products/modal_info.html',
            {"datos_act":datos_vehiculo, "product_actual":product_actual, "titulo":"Info de Producto", 
            "listamarca":listamarca, "listamodelo": listamodelo, "listacolor":listacolor})

def delete_product(request, product_actual):
    vehiculo.objects.filter(id_vehiculo=product_actual).delete()
    return redirect("../productos")

def mark_and_model(request, marcaModelo_actual = 0, tipo_carga = 0):
    listamarca = marca.objects.all()
    if tipo_carga==0:
        titulo = 'Nueva Marca'
    else:
        titulo = 'Nuevo Modelo'
    if request.method=="GET":
        marca_actual=marca.objects.filter(id_marca=marcaModelo_actual).exists()
        if marca_actual:
            datos_marca_modelo=marca.objects.filter(id_marca=marca_actual).first()
            return validar(request, 'sections/products/mark_and_model.html',
            {"datos_act":datos_marca_modelo, "marca_actual":marca_actual, "titulo":titulo, 
            "marcaModelo_actual":marcaModelo_actual, "tipo_carga": tipo_carga, "listamarca":listamarca})
        else:
            return validar(request, "sections/products/mark_and_model.html",
            {"nombre_completo":request.session.get("nombre_completo"), "marca_actual":marca_actual, 
            "titulo":titulo, "marcaModelo_actual":marcaModelo_actual, "tipo_carga": tipo_carga, "listamarca":listamarca})

    if request.method=="POST":
        marcas = marca.objects.all()
        if marcaModelo_actual==0:
            if tipo_carga==0:
                marca_nueva=marca(descripcion_marca=request.POST.get('marca')) 
                marca_nueva.save()
            else:
                modelo_nuevo=modelo(descripcion_modelo=request.POST.get('modelo'),
                id_marca_id=request.POST.get('marca'))
                modelo_nuevo.save()
        else:
            marcaModelo_actual=usuarios.objects.get(descripcion_marca=marcaModelo_actual)
            marcaModelo_actual.usuario=request.POST.get("modelo")
            print(marcaModelo_actual)
            marcaModelo_actual.save()

    return redirect('../../edit_product/0')
        

def informes(request):
    return validar(request, 'sections/informs.html')

def factura(request):
    return validar(request, 'sections/invoice.html')

def config(request):
    return validar(request, 'sections/config.html')

def users(request):
    listatabla = usuarios.objects.all()
    tipo_usu = tipo_usuario.objects.all()
    return validar(request, 'sections/config/users.html',{"listatabla":listatabla, "tipo_usu":tipo_usu})

def edit_user(request, usu_actual=0):
    tipo_usu = tipo_usuario.objects.all()
    if request.method=="GET":
        usuario_actual=usuarios.objects.filter(id_usuario=usu_actual).exists()
        if usuario_actual:
            datos_usuario=usuarios.objects.filter(id_usuario=usu_actual).first()
            return validar(request, 'sections/config/modal_user.html',
            {"datos_act":datos_usuario, "usu_actual":usu_actual, "titulo":"Editar Usuario", "tipo_usu":tipo_usu})
        else:
            return validar(request, "sections/config/edit_user.html",
            {"nombre_completo":request.session.get("nombre_completo"), "usu_actual":usu_actual, "titulo":"Cargar Usuario", "tipo_usu":tipo_usu})

    if request.method=="POST":
        if usu_actual==0:
            usuario_nuevo=usuarios(usuario=request.POST.get('usuario'),
            clave=request.POST.get('clave'), 
            nombre_completo=request.POST.get("nombre_completo"),
            tipo_usuario=request.POST.get("tipo_usuario"))
            usuario_nuevo.save()
        else:
            usuario_actual=usuarios.objects.get(id_usuario=usu_actual)
            usuario_actual.nombre_completo=request.POST.get("nombre_completo")
            usuario_actual.usuario=request.POST.get("usuario")
            usuario_actual.clave=request.POST.get("clave")
            usuario_actual.tipo_usuario=request.POST.get("tipo_usuario")
            print(usuario_actual.tipo_usuario)
            usuario_actual.save()
        
        return redirect("../users")

def delete_user(request, usu_actual):
    usuarios.objects.filter(id_usuario=usu_actual).delete()
    return redirect("../users")

def cancelar_pagare(request):
    return render(request, 'pay-fee.html')

def clientes(request, mode=0):
    listaclientes = cliente.objects.all()
    listadocumentos = tipo_documento.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()
    if mode == 0:
        buttonText="Ver deshabilitados"
        urlSwitch=1
    else:
        buttonText="Ocultar deshabilitados"
        urlSwitch=0
    return validar(request, 'sections/clients/clients.html',
    {"listadocumentos":listadocumentos, "listapais":listapais, 
    "listaciudad":listaciudad, "listaclientes":listaclientes, 
    "buttonText":buttonText, "urlSwitch":urlSwitch, "mode":mode})

def edit_client(request, clie_actual=0):
    listatipodoc = tipo_documento.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()
    if request.method=="GET":
        cliente_actual=cliente.objects.filter(id_cliente=clie_actual).exists()
        if cliente_actual:
            datos_cliente=cliente.objects.filter(id_cliente=clie_actual).first()
            return validar(request, 'sections/clients/modal_client.html',
            {"datos_act":datos_cliente, "clie_actual":clie_actual, "titulo":"Editar un Cliente", 
            "listatipodoc":listatipodoc, "listapais":listapais, "listaciudad":listaciudad})
        else:
            return validar(request, "sections/clients/edit_client.html", {"titulo":"Cargar nuevo Cliente",
            "listatipodoc":listatipodoc, "listapais":listapais, "listaciudad":listaciudad, "clie_actual": clie_actual})

    if request.method=="POST":
        if clie_actual==0:
            cliente_nuevo=cliente(documento_cliente=request.POST.get('documento_cliente'),
            nombre_cliente=request.POST.get('nombre_cliente'),
            apellido_cliente=request.POST.get("apellido_cliente"),
            telefono_cliente=request.POST.get("telefono_cliente"),
            genero_cliente=request.POST.get("genero_cliente"),
            estado_cliente=0,
            id_tipo_documento_id=request.POST.get("tipo_documento"),
            id_pais_id=request.POST.get("pais"),
            id_ciudad_id=request.POST.get("ciudad"))
            cliente_nuevo.save()
        else:
            cliente_actual=cliente.objects.get(id_cliente=clie_actual)
            cliente_actual.documento_cliente=request.POST.get("documento_cliente")
            cliente_actual.nombre_cliente=request.POST.get("nombre_cliente")
            cliente_actual.apellido_cliente=request.POST.get("apellido_cliente")
            cliente_actual.telefono_cliente=request.POST.get("telefono_cliente")
            cliente_actual.genero_cliente=request.POST.get("genero_cliente")
            cliente_actual.id_tipo_documento_id=request.POST.get("tipo_documento")
            cliente_actual.id_pais_id=request.POST.get("pais")
            cliente_actual.id_ciudad_id=request.POST.get("ciudad")
            cliente_actual.save()
        return redirect("../clientes/0")

def disable_client(request, clie_actual, option):
    print(clie_actual)
    cliente_actual=cliente.objects.get(id_cliente=clie_actual)
    cliente_actual.estado_cliente=option
    cliente_actual.save()
    return redirect("../../clientes/0")


def parameters_modal_client(request, paisCiudad_actual=0, tipo_carga=0):
    listapais = pais.objects.all()
    if tipo_carga==0:
        titulo = 'Nuevo Tipo Documento'
    elif tipo_carga==1:
        titulo = 'Nuevo País'
    else:
        titulo = 'Nueva Ciudad'
    if request.method=="GET":
        pais_actual=pais.objects.filter(id_pais=paisCiudad_actual).exists()
        if pais_actual:
            datos_pais_ciudad=pais.objects.filter(id_pais=paisCiudad_actual).first()
            return validar(request, 'sections/clients/parameters_modal_client.html',
            {"datos_act":datos_pais_ciudad, "pais_actual":pais_actual, "titulo":titulo, 
            "paisCiudad_actual":paisCiudad_actual, "tipo_carga": tipo_carga, "listapais":listapais})
        else:
            return validar(request, "sections/clients/parameters_modal_client.html",
            {"nombre_completo":request.session.get("nombre_completo"), "pais_actual":pais_actual, 
            "titulo":titulo, "paisCiudad_actual":paisCiudad_actual, "tipo_carga": tipo_carga, "listapais":listapais})

    if request.method=="POST":
        listapais = pais.objects.all()
        if paisCiudad_actual==0:
            if tipo_carga==0:
                tipo_documento_nuevo=tipo_documento(descripcion_tipo_documento=request.POST.get('tipo_documento'))
                tipo_documento_nuevo.save()
            elif tipo_carga==1:
                pais_nuevo=pais(descripcion_pais=request.POST.get('pais')) 
                pais_nuevo.save()
            else:
                ciudad_nueva=ciudad(descripcion_ciudad=request.POST.get('ciudad'),
                id_pais_id=request.POST.get('pais'))
                ciudad_nueva.save()
        else:
            paisCiudad_actual=usuarios.objects.get(descripcion_pais=paisCiudad_actual)
            paisCiudad_actual.usuarios=request.POST.get("modelo")
            print(paisCiudad_actual)
            paisCiudad_actual.save()

    return redirect('../../edit_client/0')