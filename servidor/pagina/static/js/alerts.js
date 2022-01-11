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
            }
            
        }
    })
}

//funcion que muestra una alerta para confirmar los cambios
async function alertaConfirmar(url, args) {
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
            }
            return true
        }
        return false
    })
}

function alerta(args){
    Swal.fire({
        title: args.TITLE,
        text: args.TEXT,
        icon: args.ICON,
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'Aceptar',
    }).then((result) => {

    })
}
