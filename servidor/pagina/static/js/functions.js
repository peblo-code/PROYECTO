window.onload = function(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
      dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
      mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaActual').value=ano+"-"+mes+"-"+dia;
}

function validarFormularioEdicion() {
  let inputs = document.getElementsByClassName("form-control")

  document.getElementById("btnCarga")
  .addEventListener("click", (evt) => {
      let flag = true
      for(let i=0; i < inputs.length; i++) {
          if(inputs[i].value === '') {
              alerta(argsValidacion)
              flag = false
              i = inputs.length
          }
      } if(flag) {
          return alertaConfirmar('',argsModal)
      }

  })

  var argsValidacion = {
    TITLE: 'Ups!', 
    TEXT: 'Por favor, complete todos los campos',
    ICON: 'error', 
  }
}