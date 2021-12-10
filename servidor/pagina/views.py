from django.shortcuts import redirect, render
from pagina.models import usuarios
from pagina.models import tipo_usuario
from pagina.models import vehiculo
from pagina.models import marca
from pagina.models import modelo
from pagina.models import color

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
                return render(request, 'login.html', {"mensaje": "Usuario o contraseña incorrecto"})
        else:
            return render(request, 'login.html', {"mensaje": "Usuario o contraseña incorrecto"})

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
            return validar(request, 'sections/config/edit_user.html',
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

def nuevo_cliente(request):
    return render(request, 'new-client.html')
