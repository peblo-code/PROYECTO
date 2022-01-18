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
    listaproducto = vehiculo.objects.all()
    if request.method=="GET":
        vehiculo_actual=vehiculo.objects.filter(id_vehiculo=product_actual).exists()
        if vehiculo_actual:
            datos_vehiculo=vehiculo.objects.filter(id_vehiculo=product_actual).first()
            return validar(request, 'sections/products/modal_product.html',
            {"datos_act":datos_vehiculo, "product_actual":product_actual, "titulo":"Editar un Producto", 
            "listamarca":listamarca, "listamodelo": listamodelo, "listacolor":listacolor, "listaproducto":listaproducto})
        else:
            return validar(request, "sections/products/edit_product.html", {"titulo":"Cargar nuevo Producto",
            "listamarca":listamarca, "listamodelo": listamodelo, "listacolor": listacolor, "product_actual": product_actual, "listaproducto":listaproducto})

    if request.method=="POST":
        if product_actual==0:
            vehiculo_nuevo=vehiculo(id_marca_id=request.POST.get('marca'),
            id_modelo_id=request.POST.get('modelo'), 
            id_color_id=request.POST.get("color"),
            transmision_vehiculo=request.POST.get("transmision"),
            motor_vehiculo=request.POST.get("motor"),
            anio_vehiculo=request.POST.get("anio"),
            nro_chassis_vehiculo=request.POST.get("chasis"),
            precio_costo=request.POST.get("costo").replace(".","") ,
            precio_venta=request.POST.get("venta").replace(".","") ,
            estado_vehiculo=1)
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
            vehiculo_actual.precio_costo=request.POST.get("costo").replace(".","")
            vehiculo_actual.precio_venta=request.POST.get("venta").replace(".","")
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

def mark_and_model(request, marcaModelo_actual = 0, tipo_carga = 0, redirigir = 0): #Funcion reutilizada en marca, modelo y color
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all() 
    if tipo_carga==0:   #Se detecta el tipo de carga
        titulo = 'Nueva Marca'
        listaparametros = listamarca
    elif tipo_carga==1:
        titulo = 'Nuevo Modelo'
        listaparametros = listamodelo
    else:
        titulo = 'Nuevo Color'
        listaparametros = listacolor
    if request.method=="GET":
        marca_actual=marca.objects.filter(id_marca=marcaModelo_actual).exists()
        if marca_actual:    #Se retornan los datos existentes para actualizar
            datos_marca_modelo=marca.objects.filter(id_marca=marca_actual).first()
            if redirigir == 0:  #REDIRIGIR A MODAL DE MARCA Y MODELO
                url = 'sections/products/mark_and_model.html'
            elif redirigir == 1: #REDIRIGIR A MARCA
                url = 'sections/config/parameters_products/mark.html'
            elif redirigir == 2: #REDIRIGIR A MODELO
                url = 'sections/config/parameters_products/models.html'
            else:   #REDIRIGIR A COLOR
                url = 'sections/config/parameters_products/colors.html'
            return validar(request, "sections/products/mark_and_model.html",
            {"datos_act":datos_marca_modelo, "marca_actual":marca_actual, "titulo":titulo, #RETURN A VISTA DE ACTUALIZAR
            "marcaModelo_actual":marcaModelo_actual, "tipo_carga": tipo_carga, "redirigir":redirigir,
            "listaparametros":listaparametros})
        else:   #Pasa a crear la marca o modelo
            return validar(request, "sections/products/mark_and_model.html",
            {"nombre_completo":request.session.get("nombre_completo"), "marca_actual":marca_actual, #RETURN A VISTA DE CARGA
            "titulo":titulo, "marcaModelo_actual":marcaModelo_actual, "tipo_carga": tipo_carga, "redirigir":redirigir,
            "listaparametros":listaparametros, "listamarca":listamarca})

    if request.method=="POST":
        #Redirige luego de hacer la carga
        if redirigir == 0:
            urlPost = '../../../edit_product/0'
        elif redirigir == 1:
            urlPost = '../../../mark'
        elif redirigir == 2:
            urlPost = '../../../models'
        else:
            urlPost = '../../../colors'
        
        redirigir = 0

        if marcaModelo_actual==0:
            if tipo_carga==0:
                marca_nueva=marca(descripcion_marca=request.POST.get('marca')) 
                marca_nueva.save()
                return redirect(urlPost)
            elif tipo_carga==1:
                modelo_nuevo=modelo(descripcion_modelo=request.POST.get('modelo'),
                id_marca_id=request.POST.get('marca'))
                modelo_nuevo.save()
                return redirect(urlPost)
            else:
                color_nuevo=color(descripcion_color=request.POST.get('color'))
                color_nuevo.save()
                return redirect(urlPost)
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

def parameters_products(request):
    return validar(request, 'sections/config/parameters_products.html')

def parameters_clients(request):
    return validar(request, 'sections/config/parameters_clients.html')

def mark(request):
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    return validar(request, 'sections/config/parameters_products/mark.html',{"listamarca":listamarca, "listamodelo":listamodelo})

def edit_mark(request, mark_actual=0):
    listamarca = marca.objects.all()
    if request.method=="GET":
        listamarca = marca.objects.all()
        marca_actual=marca.objects.filter(id_marca=mark_actual).exists()
        if marca_actual:
            datos_marca=marca.objects.filter(id_marca=mark_actual).first()
            return validar(request, 'sections/config/parameters_products/mark/edit_mark.html',
            {"datos_act":datos_marca, "mark_actual":mark_actual, "titulo": "Editar Marca", "listamarca":listamarca})
    if request.method=="POST":
        marca_actual=marca.objects.get(id_marca=mark_actual)
        marca_actual.descripcion_marca=request.POST.get("marca")
        marca_actual.save()
    return redirect('../mark')

def edit_color(request, color_actual=0):
    if request.method=="GET":
        colors_actual=color.objects.filter(id_color=color_actual).exists()
        if colors_actual:
            datos_color=color.objects.filter(id_color=color_actual).first()
            return validar(request, 'sections/config/parameters_products/color/edit_color.html',
            {"datos_act":datos_color, "color_actual":color_actual, "titulo": "Editar color"})
    if request.method=="POST":
        colors_actual=color.objects.get(id_color=color_actual)
        colors_actual.descripcion_color=request.POST.get("color")
        colors_actual.save()
    return redirect('../color')

def models(request):
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    return validar(request, 'sections/config/parameters_products/models.html',{"listamarca":listamarca,"listamodelo":listamodelo})

def colors(request):
    listaproducto = vehiculo.objects.all()
    listacolor = color.objects.all()
    return validar(request, 'sections/config/parameters_products/colors.html',{"listaproducto":listaproducto, "listacolor":listacolor})

def delete_color(request, color_actual):
    color.objects.filter(id_color=color_actual).delete()
    return redirect("../color")

def delete_mark(request, mark_actual):
    marca.objects.filter(id_marca=mark_actual).delete()
    return redirect("../mark")

def delete_model(request, model_actual):
    modelo.objects.filter(id_modelo=model_actual).delete()
    return redirect("../models")

def document(request):
    listacliente = cliente.objects.all()
    listadocumento = tipo_documento.objects.all()
    return validar(request, 'sections/config/parameters_clients/documents.html',{"listacliente":listacliente, "listadocumento":listadocumento})

def delete_document(request, document_actual):
    tipo_documento.objects.filter(id_tipo_documento=document_actual).delete()
    return redirect("../document")

def country(request):
    listacliente = cliente.objects.all()
    listapais = pais.objects.all()
    return validar(request, 'sections/config/parameters_clients/country.html',{"listacliente":listacliente, "listapais":listapais})

def delete_country(request, country_actual):
    pais.objects.filter(id_pais=country_actual).delete()
    return redirect("../country")

def city(request):
    listacliente = cliente.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()
    return validar(request, 'sections/config/parameters_clients/city.html',{"listacliente":listacliente, "listapais":listapais, "listaciudad":listaciudad})

def delete_city(request, city_actual):
    ciudad.objects.filter(id_ciudad=city_actual).delete()
    return redirect("../city")

def users(request):
    listatabla = usuarios.objects.all()
    tipo_usu = tipo_usuario.objects.all()
    return validar(request, 'sections/config/users.html',{"listatabla":listatabla, "tipo_usu":tipo_usu})

def edit_user(request, usu_actual=0):
    tipo_usu = tipo_usuario.objects.all()
    listausuario = usuarios.objects.all()
    if request.method=="GET":
        usuario_actual=usuarios.objects.filter(id_usuario=usu_actual).exists()
        if usuario_actual:
            datos_usuario=usuarios.objects.filter(id_usuario=usu_actual).first()
            return validar(request, 'sections/config/modal_user.html',
            {"datos_act":datos_usuario, "usu_actual":usu_actual, "titulo":"Editar Usuario", "tipo_usu":tipo_usu, "listausuario":listausuario})
        else:
            return validar(request, "sections/config/edit_user.html",
            {"nombre_completo":request.session.get("nombre_completo"), "usu_actual":usu_actual, "titulo":"Cargar Usuario", "tipo_usu":tipo_usu, "listausuario":listausuario})

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
    listacliente = cliente.objects.all()
    if request.method=="GET":
        cliente_actual=cliente.objects.filter(id_cliente=clie_actual).exists()
        if cliente_actual:
            datos_cliente=cliente.objects.filter(id_cliente=clie_actual).first()
            return validar(request, 'sections/clients/modal_client.html',
            {"datos_act":datos_cliente, "clie_actual":clie_actual, "titulo":"Editar un Cliente", 
            "listatipodoc":listatipodoc, "listapais":listapais, "listaciudad":listaciudad, "listacliente":listacliente})
        else:
            return validar(request, "sections/clients/edit_client.html", {"titulo":"Cargar nuevo Cliente",
            "listatipodoc":listatipodoc, "listapais":listapais, "listaciudad":listaciudad, "clie_actual": clie_actual, "listacliente":listacliente})

    if request.method=="POST":
        if clie_actual==0:
            cliente_nuevo=cliente(documento_cliente=request.POST.get('documento_cliente').replace(".",""),
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
            cliente_actual.documento_cliente=request.POST.get("documento_cliente").replace(".","")
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


def parameters_modal_client(request, paisCiudad_actual=0, tipo_carga=0, redirigir=0):
    listadocumento = tipo_documento.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()
    if tipo_carga==0:
        titulo = 'Nuevo Tipo Documento'
        listaparametros = listadocumento
    elif tipo_carga==1:
        titulo = 'Nuevo País'
        listaparametros = listapais
    else:
        titulo = 'Nueva Ciudad'
        listaparametros = listaciudad
    if request.method=="GET":
        if tipo_carga==0:
            datos_actual = tipo_documento.objects.filter(id_tipo_documento=paisCiudad_actual).exists()
        elif tipo_carga==1:
            datos_actual = pais.objects.filter(id_pais=paisCiudad_actual).exists()
        else:
            datos_actual = ciudad.objects.filter(id_ciudad=paisCiudad_actual).exists()
        if datos_actual:
            if tipo_carga==0:
                datos = tipo_documento.objects.filter(id_tipo_documento=paisCiudad_actual).first()
            elif tipo_carga==1:
                datos = pais.objects.filter(id_pais=paisCiudad_actual).first()
            else:
                datos = ciudad.objects.filter(id_ciudad=paisCiudad_actual).first()
            return validar(request, 'sections/clients/parameters_modal_client.html',
            {"datos_act":datos, "datos_actual":datos_actual, "titulo":titulo, 
            "paisCiudad_actual":paisCiudad_actual, "tipo_carga": tipo_carga, "redirigir":redirigir, "listaparametros":listaparametros, "listapais":listapais})
        else:
            return validar(request, "sections/clients/parameters_modal_client.html",
            {"nombre_completo":request.session.get("nombre_completo"), "datos_actual":datos_actual, 
            "titulo":titulo, "paisCiudad_actual":paisCiudad_actual, "tipo_carga": tipo_carga, "redirigir":redirigir, "listaparametros":listaparametros, "listapais":listapais})

    if request.method=="POST":
        if redirigir == 0:
            url = '../../../edit_client/0'
        elif redirigir == 1:
            url = '../../../document'
        elif redirigir == 2:
            url = '../../../country'
        elif redirigir == 3:
            url = '../../../city'

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
            if tipo_carga==0:
                tipo_documento_actual=tipo_documento.objects.get(id_tipo_documento=paisCiudad_actual)
                tipo_documento_actual.descripcion_tipo_documento=request.POST.get("tipo_documento")
                tipo_documento_actual.save()

            elif tipo_carga==1:
                pais_actual=pais.objects.get(id_pais=paisCiudad_actual)
                pais_actual.descripcion_pais=request.POST.get("pais")
                pais_actual.save()

            elif tipo_carga==2:
                ciudad_actual=ciudad.objects.get(id_ciudad=paisCiudad_actual)
                ciudad_actual.descripcion_ciudad=request.POST.get("ciudad")
                ciudad_actual.save()

    return redirect(url)