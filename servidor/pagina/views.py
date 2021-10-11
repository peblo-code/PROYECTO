from django.shortcuts import redirect, render
from pagina.models import usuarios

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.session.get("id_usuario"):
            return redirect("inicio")
        else:
            return render(request, 'index.html')

    if request.method == 'POST':
        v_usuario = request.POST.get("usuario")
        v_clave = request.POST.get("clave")
        usuario_actual = usuarios.objects.filter(usuario=v_usuario).exists()
        if usuario_actual:
            datos_usuario=usuarios.objects.filter(usuario=v_usuario).first()
            if getattr(datos_usuario, "clave") == v_clave:
                request.session["cod_usuario"]=getattr(datos_usuario, "cod_usuario")
                request.session["nombre_completo"]=getattr(datos_usuario, "nombre_completo")
                return redirect("inicio")
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')

def inicio(request):
    return render(request, 'index.html')