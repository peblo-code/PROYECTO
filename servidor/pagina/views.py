from django.shortcuts import redirect, render
from pagina.models import usuarios
from pagina.models import tipo_usuario

# Create your views here.
def validar(request, pageSuccess, parameters={}):
    if request.session.get("id_usuario"):
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
    return validar(request, 'sections/new-product.html')

def busqueda_producto(request):
    return validar(request, 'sections/search.html')

def informes(request):
    return validar(request, 'sections/informs.html')

def factura(request):
    return validar(request, 'sections/invoice.html')

def config(request):
    return validar(request, 'sections/config.html')

def users(request):
    listatabla = usuarios.objects.all()
    return validar(request, 'sections/config/users.html',{"listatabla":listatabla})

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
            clave=request.POST.get('clave'), nombre_completo=request.POST.get("nombre_completo"),
            tipo_usuario=request.POST.get(tipo_usuario))
            usuario_nuevo.save()
        else:
            usuario_actual=usuarios.objects.get(id_usuario=usu_actual)
            usuario_actual.nombre_completo=request.POST.get("nombre_completo")
            usuario_actual.usuario=request.POST.get("usuario")
            usuario_actual.clave=request.POST.get("clave")
            usuario_actual.tipo_usuario=request.POST.get("tipo_usuario")
            usuario_actual.save()
        
        return redirect("../users")

def delete_user(request, usu_actual):
    usuarios.objects.filter(id_usuario=usu_actual).delete()
    return redirect("../users")

def cancelar_pagare(request):
    return render(request, 'pay-fee.html')

def nuevo_cliente(request):
    return render(request, 'new-client.html')
