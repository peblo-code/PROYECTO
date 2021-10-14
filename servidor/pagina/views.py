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
    return render(request, 'header.html', {"nombre_completo": request.session.get("nombre_completo")})

def salir(request):
    request.session.flush()
    return redirect("./")