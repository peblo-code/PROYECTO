from django.shortcuts import redirect, render
from pagina.models import usuarios

# Create your views here.
def validar(request, pageSuccess):
    if request.session.get("id_usuario"):
        return render(request, pageSuccess, {"nombre_completo": request.session.get("nombre_completo")})
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
    return validar(request, 'index.html')

def header(request):
    return render(request, 'header.html')

def salir(request):
    request.session.flush()
    return redirect("./")

def productos(request):
    return render(request, 'sections/new-product.html')

def busqueda_producto(request):
    return render(request, 'sections/search.html')

def informes(request):
    return render(request, 'sections/informs.html')

def factura(request):
    return render(request, 'sections/invoice.html')

def config(request):
    return validar(request, 'sections/config.html')

def users(request):
    listatabla = usuarios.objects.all()
    return render(request, 'sections/config/users.html',{"listatabla":listatabla, "usuario_actual": request.session["nombre_completo"]})

def edit_user(request, usu_actual=0):
    if request.method=="GET":
        usuario_actual=usuarios.objects.filter(id_usuario=usu_actual).exists()
        if usuario_actual:
            datos_usuario=usuarios.objects.filter(id_usuario=usu_actual).first()
            return render(request, 'sections/config/edit_user.html',
            {"datos_act":datos_usuario, "usu_actual":usu_actual})
        else:
            return render(request, "sections/config/edit_user.html",
            {"nombre_completo":request.session.get("nombre_completo"), "usu_actual":usu_actual})

    if request.method=="POST":
        if usu_actual==0:
            usuario_nuevo=usuarios(usuario=request.POST.get('usuario'),
            clave=request.POST.get('clave'), nombre_completo=request.POST.get("nombre_completo"))
            usuario_nuevo.save()
        else:
            usuario_actual=usuarios.objects.get(id_usuario=usu_actual)
            usuario_actual.nombre_completo=request.POST.get("nombre_completo")
            usuario_actual.usuario=request.POST.get("usuario")
            usuario_actual.clave=request.POST.get("clave")
            usuario_actual.save()
        
        return redirect('../users')

def delete_user(request, usu_actual):
    usuarios.objects.filter(id_usuario=usu_actual).delete()
    return redirect("../users")

def cancelar_pagare(request):
    return render(request, 'pay-fee.html')

def nuevo_cliente(request):
    return render(request, 'new-client.html')
