 //CODIGO DE VALIDACION

function verificarFormulario(form) {
    args = {
        TITLE: "Ups!",
        TEXT: "No se han podido registrar los datos. Por favor, asegúrese de que estén correctos.",
        ICON: "warning"
    }
    if(document.getElementById("alert-error")) {
        alerta(args)
        return false
    }

}


function validarFormulario(divValor, flag, message) {
    debugger
    //bandera
    divValor = document.getElementById(divValor)
    function alertMessage(message){
        var alert = 
        `<div class="alert alert-danger d-flex align-items-center" role="alert" id="alert-error" style="margin-bottom: 0px">
            <div>
                ${message}
            </div>
        </div>`
        return alert
    }

    if(flag && !document.getElementById("alert-error")) {
       divValor.style = "display: inline"
       divValor.innerHTML += alertMessage(message)
    } else if(document.getElementById("alert-error") && flag == false) {
       divValor.removeChild(document.getElementById("alert-error"))
       divValor.style = "display: none"
    }
    
    if(flag) {
        return false;
    } else {
        return true;
    }
 }

 function validarFormularioEdicion(validacion, formValidar) {
    let inputs = document.getElementsByClassName(formValidar)
    console.log("estoy en la validacion")
    debugger
    
    let flag = true
    for(let i=0; i < inputs.length; i++) {
        if(inputs[i].value === '' || inputs[i].value == undefined) {
            alerta(argsValidacion)
            flag = false
            i = inputs.length
        }
    } if(flag && validacion) {
        return alertaConfirmar('',argsModal, marcaForeign='')
    } else {
        verificarFormulario()
    }
    

  }