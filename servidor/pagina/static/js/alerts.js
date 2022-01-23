function alertaConfirmarAccion(url, successPhrase, typeOfMethod, btnId) {
    let timerInterval
    Swal.fire({
        title: 'Cambios aplicados!',
        html: `El producto ha sido ${successPhrase} con éxito`,
        icon: 'success',
        timer: 2000,
        timerProgressBar: true,
        didOpen: () => {
        Swal.showLoading()
            const b = Swal.getHtmlContainer().querySelector('b')
            timerInterval = setInterval(() => {
                b.textContent = Swal.getTimerLeft()
            }, 100)
        },
        willClose: () => {
            clearInterval(timerInterval)
        }
    }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
            if(typeOfMethod == 'url') {
                window.location.href = url
            } else {
                sessionStorage.setItem('1', 1);
                if(ajx) {
                    registrarAjx(btnId, edit_name, delete_name, foreingFlag, nombreSelect)
                } else {
                    document.getElementById(btnId).submit()
                }
                $('#edicion').modal('hide');
            }
        }
    })
}

function registrarAjx(formId, edit_name, delete_name, foreingFlag, nombreSelect) {
    $.ajax({
        data: $(`#${formId}`).serialize(),
        url: $(`#${formId}`).attr('action'),
        type: $(`#${formId}`).attr('method'),
        success: function(response) {
            if(document.getElementById("tabla")) {
                actualizarTabla( JSON.parse(response.mensaje), edit_name, delete_name, foreingFlag)
            } else {
                actualizarSelect( JSON.parse(response.mensaje), nombreSelect )
            }

            var argsInsert = {
                TITLE: 'Cambios aplicados!',
                TEXT: `El producto ha sido cargado con éxito`,
                ICON: 'success'
            }
    
            if(sessionStorage.getItem('1') == 1) {
                window.onload = alerta(argsInsert)
                sessionStorage.setItem('1', 0);
            }
        },
        error: function(error) {
            
        }
    })
}

function actualizarTabla(listaTabla, edit_name, delete_name, foreingFlag) {
    $('#tabla').DataTable().destroy();
    var lista = listaTabla[listaTabla.length-1]
    var columnas = ''
    var btnEditar = ''
    var btnBorrar = ''

    for (const [clave, valor] of Object.entries(lista.fields)) {
        console.log("Iterando...");
        console.log("La clave es: " + clave);
        console.log("El valor es: " + valor);
        columnas += 
        `<td>
            ${valor}
        </td>`
    }

    if(edit_name != '') {
        btnEditar = 
        `<button onclick="abrirModalEdicion('/pagina/${edit_name}/${lista.pk}')" class="btn btn-warning">
            Editar
        </button>`
    }

    if(delete_name != '') {
        if(foreingFlag) {
            btnBorrar = 
            `<button class="btn btn-danger" onclick="detectForeing('/pagina/${delete_name}/${lista.pk}', '${lista.pk}')">
                Borrar
            </button>
            `
        } else {
            btnBorrar = 
            `<button class="btn btn-danger" onclick="alertaConfirmar('/pagina/${delete_name}/${lista.pk}', args)">
                Borrar
            </button>
            `
        }
    }

    document.getElementById("tabla").insertRow(-1).innerHTML =
    `${columnas}
    <td class="actions" style="justify-content:end">
        ${btnEditar}
        ${btnBorrar}
    </td>`;
    dataTable()
}



function actualizarSelect(listaSelect, nombreSelect) {
    var lista = listaSelect[listaSelect.length-1]

    var SELECT = document.getElementById(nombreSelect)
    const option = document.createElement('option');
    option.id = "opcion_select"
    option.value = lista.pk;
    var i = 0
    for (const [clave, valor] of Object.entries(lista.fields)) {
        if(clave.match(/descripcion/g)) {
            option.text = valor
        }
    }
    SELECT.appendChild(option);
}

//funcion que muestra una alerta para confirmar los cambios
function alertaConfirmar(url, args) {
    return Swal.fire({
        title: args.TITLE,
        text: args.TEXT,
        icon: args.ICON,
        showCancelButton: true,
        cancelButtonColor: '#d33',
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Sí, hazlo!',
    }).then((result) => {
        if(result.isConfirmed) {
            //funcion que informa al usuario lo que sucedió
            if(args.typeOfMethod == 'url') {
                alertaConfirmarAccion(url, args.successPhrase, args.typeOfMethod)
            } else {
                alertaConfirmarAccion(url, args.successPhrase, args.typeOfMethod, args.btnId, args.ajx, 
                    args.edit_name, args.delete_name, args.foreingFlag, args.nombreSelect)
            }
        }
    })
}

function alerta(args){
    return Swal.fire({
        title: args.TITLE,
        text: args.TEXT,
        icon: args.ICON,
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'Aceptar',
    }).then((result) => result)
}
