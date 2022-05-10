from ast import Not, mod
from distutils.log import error
from django.shortcuts import redirect, render
from pagina.models import *
from django.http import HttpResponse, JsonResponse, response
from django.core import serializers
from datetime import date


# Create your views here.
def auditoria(usr="", table="", id=0, flag=0):
    if flag==0:
        auditoria_nueva=auditoria(
        usuario_creacion=usr,
        fecha_creacion=date.today().isoformat(),
        id_cambio=id,
        tabla_cambio=table)
        auditoria_nueva.save()

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
        listapagaredetalle = detalle_pagare.objects.all()
        fecha_actual = date.today().isoformat()
        for pagaredetalle in listapagaredetalle:
            if int(str(pagaredetalle.fch_vencimiento_detalle_pagare)[5:7]) < int(fecha_actual[5:7]):
                if int(str(pagaredetalle.fch_vencimiento_detalle_pagare)[0:4]) == int(fecha_actual[0:4]):
                    if pagaredetalle.fch_pago_detalle_pagare is None:
                        pagare_detalle_actual=detalle_pagare.objects.get(id_pagare_detalle_pagare=pagaredetalle.id_pagare_detalle_pagare)
                        pagare_detalle_actual.intereses_pagare_detalle=(int(pagaredetalle.monto_pagare_detalle) * 0.04) * (int(fecha_actual[5:7]) - int(str(pagaredetalle.fch_vencimiento_detalle_pagare)[5:7]))
                        pagare_detalle_actual.save()



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
    listafacturacompra = factura_compra.objects.all()
    return validar(request, 'sections/products/products.html',{"listaproducto":listaproducto, "listamarca":listamarca, 
    "listamodelo": listamodelo, "listacolor":listacolor, "listafacturacompra":listafacturacompra})

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
            estado_vehiculo=0)
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
            vehiculo_actual.estado_vehiculo=0
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
        if marcaModelo_actual==0:
            if tipo_carga==0:
                marca_nueva=marca(descripcion_marca=request.POST.get('marca'))
                marca_nueva.save()
                test = serializers.serialize('json', list(listamarca))
                #return redirect(urlPost)
            elif tipo_carga==1:
                modelo_nuevo=modelo(descripcion_modelo=request.POST.get('modelo'),
                id_marca_id=request.POST.get('marca'))
                modelo_nuevo.save()
                test = serializers.serialize('json', list(listamodelo))
                #return redirect(urlPost)
            else:
                color_nuevo=color(descripcion_color=request.POST.get('color'))
                color_nuevo.save()
                test = serializers.serialize('json', list(listacolor))
                #return redirect(urlPost)
        error = 'No hay error!'
        response = JsonResponse({'mensaje':test, 'error':error})
        response.status_code = 201
        return response

def informes(request):
    return validar(request, 'sections/informs.html')

def factura(request):
    return validar(request, 'sections/invoice.html')

def compra(request):
    return validar(request, "sections/invoice/buy.html")

def venta(request):
    caja_personalizada = caja.objects.raw("SELECT id_caja, fch_apertura_caja, fch_cierre_caja, id_usuario_id FROM pagina_caja ORDER BY id_caja DESC LIMIT 1")
    estado_caja = 0 #cerrado
    for cajita in caja_personalizada:
        if cajita.fch_apertura_caja:
            estado_caja = 1 #abierto
        if cajita.fch_cierre_caja:
            estado_caja = 0 #cerrado

    return validar(request, "sections/invoice/sell.html", {
        "estado_caja": estado_caja,
    })


def factura_vender(request):
    listacliente = cliente.objects.all()
    listatimbradoparametros = timbrado_parametros.objects.all()
    listafacturaparametros = factura_parametros.objects.all()
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    listafacturaventa = factura_venta.objects.all()
    url = './get_cash/'

    if request.method == 'GET':
        return validar(request, 'sections/invoice/invoice-sell.html', {
            'listacliente': listacliente, "listatimbradoparametros":listatimbradoparametros, 
            "listaproducto": listaproducto, "listamarca": listamarca, "listamodelo": listamodelo,
            "listafacturaparametros": listafacturaparametros,
            "listacolor": listacolor,
            "listafacturaventa": listafacturaventa,
            "fecha_act": date.today().isoformat()
        })

    if request.method == 'POST':
        nueva_venta=factura_venta(
            id_cliente_id = request.POST.get('id_cliente'),
            nro_timbrado_parametros_id = request.POST.get('nro_timbrado'),
            id_vehiculo_id = request.POST.get('id_vehiculo'),
            nro_factura_venta = request.POST.get('nro_factura'),
            fch_factura_venta = date.today().isoformat(),
            condicion_factura_venta = request.POST.get('condicion_factura'),
            subtotal_factura_venta = request.POST.get('subtotal'),
            iva10_factura_venta = request.POST.get('iva10'),
            total_factura_venta = request.POST.get('total'),
            estado_factura_venta = 2,
        )
        nueva_venta.save()

        modificar_vehiculo=vehiculo.objects.get(id_vehiculo=request.POST.get('id_vehiculo'))
        modificar_vehiculo.estado_vehiculo = 2
        modificar_vehiculo.save()

        modificar_factura_parametros=factura_parametros.objects.get(id_factura_parametros=request.POST.get('id_factura_parametros'))
        modificar_factura_parametros.nro_actual_factura_parametros = int(request.POST.get('nro_factura')) + 1
        modificar_factura_parametros.save()
        if(int(request.POST.get('condicion_factura')) == 1):
            factura_personalizada = factura_venta.objects.raw("SELECT id_factura_venta FROM pagina_factura_venta ORDER BY id_factura_venta DESC LIMIT 1")
            id_factura = 0
            for facturita in factura_personalizada:
                id_factura = facturita.id_factura_venta

            nuevo_pagare=pagare(
            id_factura_venta_id = id_factura,
            id_cliente_id = request.POST.get('id_cliente'),
            deuda_total_pagare = 0,
            estado_pagare = 0,
            cancelados_pagares = 0)
            nuevo_pagare.save()

            url = './generar_pagare/'

    factura_personalizada = factura_venta.objects.raw("SELECT id_factura_venta FROM pagina_factura_venta ORDER BY id_factura_venta DESC LIMIT 1")
    id_factura = 0
    for facturita in factura_personalizada:
        id_factura = facturita.id_factura_venta


    return redirect(url + str(id_factura))

def get_cash(request, factu_actual=0):
    listafacturaventa = factura_venta.objects.all()
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    if request.method=="GET":
        factura_actual=factura_venta.objects.filter(id_factura_venta=factu_actual).exists()
        if factura_actual:
            datos_factura=factura_venta.objects.filter(id_factura_venta=factu_actual).first()
            return validar(request, 'sections/invoice/get_cash.html',
            {"datos_act":datos_factura, "factu_actual":factu_actual, "titulo":"Generar Cobro", 
             "listafacturaventa":listafacturaventa})

    if request.method=="POST":
        modificar_factura_venta=factura_venta.objects.get(id_factura_venta=factu_actual)
        modificar_factura_venta.monto_cobrado_factura_venta = float(request.POST.get("monto_cobrado").replace(",","."))
        modificar_factura_venta.estado_factura_venta = 1
        modificar_factura_venta.fch_cobrado_factura_venta = date.today().isoformat()
        modificar_factura_venta.save()

        varMarca = ""
        varModel = ""

        for factura_vent in listafacturaventa:
            for product in listaproducto:
                if product.id_vehiculo == factura_vent.id_vehiculo_id:
                    for mark in listamarca:
                        if mark.id_marca == product.id_marca_id:
                            varMarca = mark.descripcion_marca
                    for mod in listamodelo:
                        if mod.id_modelo == product.id_modelo_id:
                            varModel = mod.descripcion_modelo

        id_caja_actual=caja.objects.all().last().id_caja

        detalle_caja_actual=detalle_caja(
            id_caja_id = id_caja_actual,
            tipo_movimiento_detalle_caja = 0, #1 Representa EGRESO
            descripcion_detalle_caja = "Venta de vehiculo " + varMarca + " " + varModel,
            monto_detalle_caja = request.POST.get('monto_cobrado').replace(".","").replace(",",".")
        )
        detalle_caja_actual.save()

        
    return redirect("../factura_venta")

def imprimir_factura(request, factura_actual=0):
    factura_actual=factura_venta.objects.filter(id_factura_venta=factura_actual).exists()
    if factura_actual:
        datos_factura=factura_venta.objects.filter(id_factura_venta=factura_actual).first()
        return validar(request, 'sections/invoice/print_invoice.html',
        {
            "datos_act":datos_factura, "factura_actual":factura_actual, "titulo":"Imprimir Factura",
            "listafacturaventa":factura_venta.objects.all()
        })

    return redirect("../factura_venta")


def generar_pagare(request, factu_actual=0):
    factura_actual=factura_venta.objects.filter(id_factura_venta=factu_actual).exists()

    pagare_personalizado = pagare.objects.raw("SELECT id_pagare FROM pagina_pagare ORDER BY id_pagare DESC LIMIT 1")
    id_pagare = 0
    for pagaresito in pagare_personalizado:
        id_pagare = pagaresito.id_pagare


    if factura_actual:
        datos_factura=factura_venta.objects.filter(id_factura_venta=factu_actual).first()
        return validar(request, "sections/invoice/invoice-fee.html", {
            "factu_actual":factu_actual, 
            "id_pagare": id_pagare, 
            "datos_act":datos_factura 
            })

def invoice_fee_edit(request):
    if request.method == "POST":
        detalle_pagare_nuevo=detalle_pagare(id_pagare_id=request.POST.get('id_pagare'),
        nro_cuota_detalle_pagare=request.POST.get('nro_cuota_detalle_pagare'),
        fch_vencimiento_detalle_pagare=request.POST.get("fch_vencimiento_detalle_pagare"),
        monto_pagare_detalle=request.POST.get("monto_pagare_detalle").replace(".","").replace(",","."),
        intereses_pagare_detalle=0)
        detalle_pagare_nuevo.save()

        modificar_pagare=pagare.objects.get(id_pagare=request.POST.get('id_pagare'))
        modificar_pagare.fecha_inicio_pagare = request.POST.get('fecha_inicio')
        modificar_pagare.fecha_final_pagare = request.POST.get("fch_vencimiento_detalle_pagare")
        modificar_pagare.total_pagares = request.POST.get('nro_cuota_detalle_pagare')
        modificar_pagare.save()

    error = 'No hay error!'
    response = JsonResponse({'error':error})
    response.status_code = 201
    return response


def historial_venta(request, mode=0):
    listacliente = cliente.objects.all()
    listavehiculo = vehiculo.objects.all()
    listafacturaventa = factura_venta.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()

    return validar(request, "sections/invoice/sell_history.html", {
        "listacliente": listacliente,
        "listavehiculo": listavehiculo,
        "listafacturaventa": listafacturaventa,
        "listamarca": listamarca,
        "listamodelo": listamodelo,
        "mode": mode
    })

def historial_compra(request):
    listaproveedor = proveedor.objects.all()
    listavehiculo = vehiculo.objects.all()
    listafacturacompra = factura_compra.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()

    return validar(request, "sections/invoice/buy_history.html", {
        "listaproveedor": listaproveedor,
        "listavehiculo": listavehiculo,
        "listafacturacompra": listafacturacompra,
        "listamarca": listamarca,
        "listamodelo": listamodelo
    })

def factura_comprar(request):
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    listatimbrado = timbrado.objects.all()
    listafacturacompra = factura_compra.objects.all()

    if request.method == 'GET':

        return validar(request, 'sections/invoice/invoice-buy.html', {
            "listaproducto": listaproducto, "listamarca": listamarca, "listamodelo": listamodelo,
            "listacolor": listacolor,
            "listafacturacompra": listafacturacompra,
            "listatimbrado": listatimbrado,
            "fecha_act": date.today().isoformat()
        })

    if request.method == 'POST':
        nueva_compra=factura_compra(
            id_proveedor_id = request.POST.get('id_proveedor'),
            nro_timbrado_id = request.POST.get('nro_timbrado'),
            id_vehiculo_id = request.POST.get('id_vehiculo'),
            nro_factura_compra = request.POST.get('nro_factura'),
            fch_factura_compra = date.today().isoformat(),
            condicion_factura_compra = request.POST.get('condicion_factura')
        )
        nueva_compra.save()

        modificar_vehiculo=vehiculo.objects.get(id_vehiculo=request.POST.get('id_vehiculo'))
        modificar_vehiculo.estado_vehiculo = 1
        modificar_vehiculo.save()

    return redirect('./factura_compra')

def cash(request):
    return validar(request, "sections/invoice/cash.html")

def cash_history(request):
    listacaja = caja.objects.all()
    listausuario = usuarios.objects.all()

    return validar(request, "sections/invoice/cash_history.html", {"listacaja":listacaja, "listausuario":listausuario})

def modal_view_cash(request, caja_actual=0):
    listacajadetalle = detalle_caja.objects.all()
    
    return validar(request, "sections/invoice/modal_view_cash.html", {"listacajadetalle": listacajadetalle, "caja_actual":caja_actual, "titulo": "Detalle Caja"})

def cash_register(request):
    listacaja = caja.objects.all()
    listacajadetalle = detalle_caja.objects.all()
    listausuario = usuarios.objects.all()

    if caja.objects.all().last():
        id_ultima_caja=caja.objects.all().last().id_caja
    else:
        id_ultima_caja=1
    id_ultimo_usuario = 0

    detalle_caja_personalizada = detalle_caja.objects.raw("SELECT pagina_detalle_caja.id_detalle_caja, sum(pagina_detalle_caja.monto_detalle_caja) AS saldo_actual FROM pagina_detalle_caja WHERE pagina_detalle_caja.id_caja_id = " + str(id_ultima_caja))
    monto_detalle_caja = 0
    for detalle_cajita in detalle_caja_personalizada:
        monto_detalle_caja = detalle_cajita.saldo_actual

    caja_personalizada = caja.objects.raw("SELECT id_caja, fch_apertura_caja, fch_cierre_caja, id_usuario_id FROM pagina_caja ORDER BY id_caja DESC LIMIT 1")
    estado_caja = 0 #cerrado
    for cajita in caja_personalizada:
        if cajita.fch_apertura_caja:
            estado_caja = 1 #abierto
        if cajita.fch_cierre_caja:
            estado_caja = 0 #cerrado
        id_ultimo_usuario = cajita.id_usuario_id

    if request.method == 'GET':
        return validar(request, "sections/invoice/cash_register.html", 
            {
                "estado_caja": estado_caja,
                "listacaja": listacaja,
                "listacajadetalle": listacajadetalle,
                "listausuario": listausuario,
                "id_caja_actual": id_ultima_caja,
                "id_ultimo_usuario": id_ultimo_usuario,
                "id_usuario": request.session.get("id_usuario"),
                "saldo_actual": monto_detalle_caja,
                "titulo":"Caja",
                "fecha_act": date.today().isoformat()
            }
        )
    
    if request.method == 'POST':

        if estado_caja == 0: #SI CAJA ESTA CERRADA
            nueva_caja=caja(
                id_usuario_id = request.POST.get('id_usuario'),
                fch_apertura_caja = date.today().isoformat(),
                inicio_caja=request.POST.get('monto_caja').replace(".","").replace(",","."),
            )
            nueva_caja.save()

            id_nueva_caja=caja.objects.all().last().id_caja

            nuevo_detalle_caja=detalle_caja(
                id_caja_id = id_nueva_caja,
                tipo_movimiento_detalle_caja = 0, #0 Representa INGRESO
                descripcion_detalle_caja = "Apertura de Caja",
                monto_detalle_caja = request.POST.get('monto_caja').replace(".","").replace(",","."),
            )

            nuevo_detalle_caja.save()

        else:  #SI CAJA ESTA ABIERTA
            id_caja_actual=caja.objects.all().last().id_caja
            monto_detalle_caja = request.POST.get('monto_caja').replace(".","").replace(",",".")

            detalle_caja_actual=detalle_caja(
                id_caja_id = id_caja_actual,
                tipo_movimiento_detalle_caja = 1, #1 Representa EGRESO
                descripcion_detalle_caja = request.POST.get('descripcion_caja'),
                monto_detalle_caja = int(monto_detalle_caja) * (-1),
            )

            detalle_caja_actual.save()
    
    return redirect('./cash_register')

def cash_detail_delete(request, detalle_caja_actual = 0):
    detalle_caja.objects.filter(id_detalle_caja=detalle_caja_actual).delete()
    return redirect("../cash_register")

def close_cash_register(request, id_caja_actual):
    detalle_caja_personalizada = detalle_caja.objects.raw("SELECT pagina_detalle_caja.id_detalle_caja, sum(pagina_detalle_caja.monto_detalle_caja) AS saldo_actual FROM pagina_detalle_caja WHERE pagina_detalle_caja.id_caja_id = " + str(id_caja_actual))
    monto_detalle_caja = 0
    for detalle_cajita in detalle_caja_personalizada:
        monto_detalle_caja = detalle_cajita.saldo_actual

    caja_actual=caja.objects.get(id_caja=id_caja_actual)
    caja_actual.fch_cierre_caja = date.today().isoformat()
    caja_actual.cierre_caja = monto_detalle_caja
    caja_actual.save()

    return redirect('../cash_register')

def config(request):
    return validar(request, 'sections/config.html')

def parameters_products(request):
    return validar(request, 'sections/config/parameters_products.html')

def parameters_clients(request):
    return validar(request, 'sections/config/parameters_clients.html')

def parameters_sell(request):
    return validar(request, "sections/config/parameters_sell.html")

def timbrado_sell(request):
    listatimbradoparametros = timbrado_parametros.objects.all()
    return validar(request, "sections/config/parameters_sell/timbrado_sell.html", 
        {
            "listatimbradoparametros": listatimbradoparametros,
        })

def factura_sell(request):
    listafacturaparametros = factura_parametros.objects.all()
    return validar(request, "sections/config/parameters_sell/factura_sell.html", 
        {
            "listafacturaparametros": listafacturaparametros
        })

def edit_timbrado_sell(request, timbrado_actual = 0):
    listatimbradoparametros = timbrado_parametros.objects.all()
    listafacturaventa = factura_venta.objects.all()

    if request.method == "GET":
        timbra_actual=timbrado_parametros.objects.filter(nro_timbrado_parametros=timbrado_actual).exists()
        if timbra_actual:
            datos_timbrado=timbrado_parametros.objects.filter(nro_timbrado_parametros=timbrado_actual).first()
            return validar(request, "sections/config/parameters_sell/edit_timbrado_sell.html", {
                "listatimbradoparametros": listatimbradoparametros,
                "listafacturaventa": listafacturaventa,
                "titulo": "Carga Timbrado Venta",
                "datos_act": datos_timbrado,
                "timbrado_actual": timbrado_actual
            })
        else:
            return validar(request, "sections/config/parameters_sell/edit_timbrado_sell.html", {
                "listatimbradoparametros": listatimbradoparametros,
                "listafacturaventa": listafacturaventa,
                "titulo": "Carga Timbrado Venta",
                "timbrado_actual": timbrado_actual
            })
    if request.method == "POST":
        if timbrado_actual == 0:
            timbrado_parametros_nuevo=timbrado_parametros(
                nro_timbrado_parametros=request.POST.get('nro_timbrado'),
                fch_vencimiento_timbrado_parametros=request.POST.get('fch_vencimiento')
            )
            timbrado_parametros_nuevo.save()
        else:
            timbrado_parametros_actual=timbrado_parametros.objects.get(nro_timbrado_parametros=timbrado_actual)
            timbrado_parametros_actual.fch_vencimiento_timbrado_parametros = request.POST.get('fch_vencimiento')
            timbrado_parametros_actual.save()

        return redirect("../timbrado_sell")

def edit_factura_sell(request, factura_actual = 0):
    listafacturaparametros = factura_parametros.objects.all()
    listatimbradoparametros = timbrado_parametros.objects.all()

    if request.method == "GET":
        timbra_actual=factura_parametros.objects.filter(id_factura_parametros=factura_actual).exists()
        if timbra_actual:
            datos_timbrado=factura_parametros.objects.filter(id_factura_parametros=factura_actual).first()
            return validar(request, "sections/config/parameters_sell/edit_factura_sell.html", {
                "listafacturaparametros": listafacturaparametros,
                "listatimbradoparametros": listatimbradoparametros,
                "titulo": "Actualizar Factura Venta",
                "datos_act": datos_timbrado,
                "factura_actual": factura_actual
            })
        else:
            return validar(request, "sections/config/parameters_sell/edit_factura_sell.html", {
                "listafacturaparametros": listafacturaparametros,
                "listatimbradoparametros": listatimbradoparametros,
                "titulo": "Carga Factura Venta",
                "factura_actual": factura_actual
            })
    if request.method == "POST":
        if factura_actual == 0:
            factura_parametros_nuevo=factura_parametros(
                nro_timbrado_parametros_id=request.POST.get('timbrado'),
                nro_inicio_factura_parametros=request.POST.get('nro_desde'),
                nro_actual_factura_parametros=request.POST.get('nro_actual'),
                nro_fin_factura_parametros=request.POST.get('nro_final')
            )
            factura_parametros_nuevo.save()
        else:
            print(factura_actual)
            factura_parametros_actual=factura_parametros.objects.get(id_factura_parametros=factura_actual)
            factura_parametros_actual.nro_timbrado_parametros_id = request.POST.get('timbrado')
            factura_parametros_actual.nro_inicio_factura_parametros = request.POST.get('nro_desde')
            factura_parametros_actual.nro_actual_factura_parametros = request.POST.get('nro_actual')
            factura_parametros_actual.nro_fin_factura_parametros = request.POST.get('nro_final')
            factura_parametros_actual.save()

        return redirect("../factura_sell")

def delete_factura_sell(request, factura_actual=0):
    factura_parametros.objects.filter(id_factura_parametros=factura_actual).delete()
    return redirect("../factura_sell")

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
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    return validar(request, 'sections/config/parameters_products/models.html',{"listamarca":listamarca,"listamodelo":listamodelo, "listaproducto": listaproducto})

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
            {"nombre_completo":request.session.get("nombre_completo"), "usu_actual":usu_actual, "titulo":"Cargar Usuario", "tipo_usu":tipo_usu,
             "listausuario":listausuario})

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
    listaclientes = cliente.objects.all()
    listadocumentos = tipo_documento.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()
    listapagare = pagare.objects.all()
    listapagaredetalle = detalle_pagare.objects.all()

    return validar(request, 'sections/pay-fee.html',
    {
        "listaclientes": listaclientes,
        "listadocumentos": listadocumentos,
        "listapais": listapais,
        "listaciudad": listaciudad,
        "listapagare": listapagare,
        "listapagaredetalle": listapagaredetalle
    })
    
def lista_pagare(request, client_actual = 0, pagare_actual = 0):
    listapagare = pagare.objects.all()
    listapagaredetalle = detalle_pagare.objects.all()
    cliente_actual=cliente.objects.filter(id_cliente=client_actual).first()

    return validar(request, "sections/pay-fee/view-fees.html", {
        "client_actual": client_actual,
        "pagare_actual": pagare_actual,
        "datos_act": cliente_actual,
        "listapagare": listapagare,
        "listapagaredetalle": listapagaredetalle
    })

def pagar_cuota(request, paga_actual=0):
    id_pagare = 0
    listacliente = cliente.objects.all()
    if request.method == "GET":
        pagare_actual=detalle_pagare.objects.filter(id_pagare_detalle_pagare=paga_actual).first()
        print(paga_actual)

        return validar(request, "sections/pay-fee/cancel-fees.html", {
            "paga_actual": paga_actual,
            "datos_act": pagare_actual,
            "titulo": "Pagar Cuota"
        })

    if request.method == "POST":
        id_pagare=request.POST.get("id_pagare")

        pag_actual=detalle_pagare.objects.filter(id_pagare_detalle_pagare=paga_actual).first()
        pagaresito=pagare.objects.filter(id_pagare=pag_actual.id_pagare_id).first()

        pagare_actual=pagare.objects.get(id_pagare=pag_actual.id_pagare_id)
        pagare_actual.cancelados_pagares = int(pagaresito.cancelados_pagares) + 1
        pagare_actual.save()

        pagare_detalle_actual=detalle_pagare.objects.get(id_pagare_detalle_pagare=paga_actual)
        pagare_detalle_actual.fch_pago_detalle_pagare=date.today().isoformat()
        pagare_detalle_actual.save()

        id_caja_actual=caja.objects.all().last().id_caja
        id_cliente_pagare=pagare.objects.all().last().id_cliente_id
        id_pagaresito=pagare.objects.all().last().id_pagare
        nombrecompleto = ""

        for client in listacliente:
            if client.id_cliente == id_cliente_pagare:
                nombrecompleto = str(client.nombre_cliente) + " " + str(client.apellido_cliente)

        detalle_caja_actual=detalle_caja(
            id_caja_id = id_caja_actual,
            tipo_movimiento_detalle_caja = 0, #1 Representa EGRESO
            descripcion_detalle_caja = "Pago de cuota de " + nombrecompleto,
            monto_detalle_caja = request.POST.get('monto_cobrado').replace(".","").replace(",",".")
        )
        detalle_caja_actual.save() 

       
    return redirect("../lista_pagare/" + str(id_cliente_pagare) + "/" + str(id_pagaresito))


def personas(request):
    return validar(request,'sections/people.html')

def proveedores(request, mode=0):
    listaproveedor = proveedor.objects.all()

    if mode == 0:
        buttonText="Ver deshabilitados"
        urlSwitch=1
    else:
        buttonText="Ocultar deshabilitados"
        urlSwitch=0

    return validar(request, 'sections/people/supplier.html', {"listaproveedor": listaproveedor, 
    "urlSwitch":urlSwitch, "buttonText":buttonText, "mode":mode})

def edit_proveedor(request, proveedor_actual = 0):
    listaproveedor = proveedor.objects.all()
    if request.method=="GET":
        prov_actual=proveedor.objects.filter(id_proveedor=proveedor_actual).exists()
        if prov_actual:
            datos_proveedor=proveedor.objects.filter(id_proveedor=proveedor_actual).first()
            return validar(request, 'sections/people/modal_supplier.html',
            {"datos_act":datos_proveedor, "proveedor_actual":proveedor_actual, "titulo":"Editar un Proveedor",
            "listaproveedor":listaproveedor})
        else:
            return validar(request, "sections/people/edit_supplier.html", {"titulo":"Cargar nuevo Proveedor",
            "listaproveedor":listaproveedor, "proveedor_actual": proveedor_actual})

    if request.method=="POST":
        if proveedor_actual==0:
            proveedor_nuevo=proveedor(ruc_proveedor=request.POST.get('ruc_proveedor').replace(".",""),
            razon_social_proveedor=request.POST.get('razon_social_proveedor'),
            telefono_proveedor=request.POST.get("telefono_proveedor"),
            direccion_proveedor=request.POST.get("direccion_proveedor"),
            estado_proveedor=0)
            proveedor_nuevo.save()
        else:
            proveedor_actual=proveedor.objects.get(id_proveedor=proveedor_actual)
            proveedor_actual.ruc_proveedor=request.POST.get("ruc_proveedor").replace(".","")
            proveedor_actual.razon_social_proveedor=request.POST.get("razon_social_proveedor")
            proveedor_actual.telefono_proveedor=request.POST.get("telefono_proveedor")
            proveedor_actual.direccion_proveedor=request.POST.get("direccion_proveedor")
            proveedor_actual.save()
        return redirect("../proveedores/0")

def modal_view_proveedor(request):
    listaproveedor = proveedor.objects.all()
    listatimbrado = timbrado.objects.all()

    return validar(request, 'sections/invoice/modal_view_supplier.html', {"listaproveedor":listaproveedor, "listatimbrado":listatimbrado, "titulo": "Proveedores"})

def modal_view_cliente(request):
    listacliente = cliente.objects.all()
    listadocumentos = tipo_documento.objects.all()
    listapais = pais.objects.all()
    listaciudad = ciudad.objects.all()

    return validar(request, 'sections/invoice/modal_view_client.html', 
    {
        "listacliente":listacliente, 
        "listadocumentos":listadocumentos,
        "listapais": listapais,
        "listaciudad": listaciudad, 
        "titulo": "Clientes"
    })

def timbrados(request, proveedor_actual=0):
    listatimbrado = timbrado.objects.all()
    if request.method == "GET":
        return validar(request, 'sections/people/timbrado/timbrado.html', {"listatimbrado": listatimbrado, "proveedor_actual":proveedor_actual})

    elif request.method == "POST":
        timbrado_nuevo=timbrado(nro_timbrado=request.POST.get('nro_timbrado'),
        id_proveedor_id=proveedor_actual,
        fch_vencimiento_timbrado=request.POST.get("fch_vencimiento_timbrado"))
        timbrado_nuevo.save()
        
        test = serializers.serialize('json', list(listatimbrado))
        error = 'No hay error!'
        response = JsonResponse({'mensaje':test, 'error':error})
        response.status_code = 201
        return response 

def delete_timbrado(request, timbra_actual=0):
    timbrado.objects.filter(nro_timbrado=timbra_actual).delete()
    return redirect("../proveedores/0")

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
    return validar(request, 'sections/people/clients.html',
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
            return validar(request, 'sections/people/modal_client.html',
            {"datos_act":datos_cliente, "clie_actual":clie_actual, "titulo":"Editar un Cliente", 
            "listatipodoc":listatipodoc, "listapais":listapais, "listaciudad":listaciudad, "listacliente":listacliente})
        else:
            return validar(request, "sections/people/edit_client.html", {"titulo":"Cargar nuevo Cliente",
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

def disable_proveedor(request, proveedor_actual, option):
    proveedor_actual=proveedor.objects.get(id_proveedor=proveedor_actual)
    proveedor_actual.estado_proveedor=option
    proveedor_actual.save()
    return redirect("../../proveedores/0")

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
            return validar(request, 'sections/people/parameters_modal_client.html',
            {"datos_act":datos, "datos_actual":datos_actual, "titulo":titulo, 
            "paisCiudad_actual":paisCiudad_actual, "tipo_carga": tipo_carga, "redirigir":redirigir, "listaparametros":listaparametros, "listapais":listapais})
        else:
            return validar(request, "sections/people/parameters_modal_client.html",
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
                test = serializers.serialize('json', list(listadocumento))
            elif tipo_carga==1:
                pais_nuevo=pais(descripcion_pais=request.POST.get('pais')) 
                pais_nuevo.save()
                test = serializers.serialize('json', list(listapais))
            else:
                ciudad_nueva=ciudad(descripcion_ciudad=request.POST.get('ciudad'),
                id_pais_id=request.POST.get('pais'))
                ciudad_nueva.save()
                test = serializers.serialize('json', list(listaciudad))
            if redirigir == 0:
                error = 'No hay error!'
                response = JsonResponse({'mensaje':test, 'error':error})
                response.status_code = 201
                return response
            else:
                return redirect(url)
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

def reportes(request):
    return validar(request, 'sections/reports.html')

def reportes_clientes(request, mode=0):
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

    return validar(request, 'sections/reportes/reporte-cliente.html', {"listadocumentos":listadocumentos, "listapais":listapais, 
    "listaciudad":listaciudad, "listaclientes":listaclientes, 
    "buttonText":buttonText, "urlSwitch":urlSwitch, "mode":mode})

def reportes_proveedores(request, mode=0):
    listaproveedor = proveedor.objects.all()

    if mode == 0:
        buttonText="Ver deshabilitados"
        urlSwitch=1
    else:
        buttonText="Ocultar deshabilitados"
        urlSwitch=0

    return validar(request, 'sections/reportes/reporte-proveedores.html', {"listaproveedor": listaproveedor, 
    "urlSwitch":urlSwitch, "buttonText":buttonText, "mode":mode})

def reportes_caja(request):
    listacaja = caja.objects.all()
    listausuario = usuarios.objects.all()

    return validar(request, "sections/reportes/reporte-caja.html", {"listacaja":listacaja, "listausuario":listausuario})

def reportes_productos(request):
    listafacturacompra = factura_compra.objects.all()
    listafacturaventa = factura_venta.objects.all()
    listaproducto = vehiculo.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()
    listacolor = color.objects.all()
    listafacturacompra = factura_compra.objects.all()
    return validar(request, 'sections/reportes/reporte-productos.html',{"listaproducto":listaproducto, "listamarca":listamarca, 
    "listamodelo": listamodelo, "listacolor":listacolor, "listafacturacompra":listafacturacompra, "listafacturaventa":listafacturaventa})

def reportes_compras(request):
    listaproveedor = proveedor.objects.all()
    listavehiculo = vehiculo.objects.all()
    listafacturacompra = factura_compra.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()

    return validar(request, 'sections/reportes/reporte-compras.html', {
        "listaproveedor": listaproveedor,
        "listavehiculo": listavehiculo,
        "listafacturacompra": listafacturacompra,
        "listamarca": listamarca,
        "listamodelo": listamodelo
    })

def reportes_ventas(request):
    listacliente = cliente.objects.all()
    listavehiculo = vehiculo.objects.all()
    listafacturaventa = factura_venta.objects.all()
    listamarca = marca.objects.all()
    listamodelo = modelo.objects.all()

    return validar(request, 'sections/reportes/reporte-ventas.html', {
        "listacliente": listacliente,
        "listavehiculo": listavehiculo,
        "listafacturaventa": listafacturaventa,
        "listamarca": listamarca,
        "listamodelo": listamodelo,
    })

