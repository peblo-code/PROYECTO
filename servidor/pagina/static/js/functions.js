/* window.onload = function(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
      dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
      mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaActual').value=ano+"-"+mes+"-"+dia;
} */

var argsValidacion = {
  TITLE: 'Ups!', 
  TEXT: 'Por favor, complete todos los campos',
  ICON: 'error', 
}


function format(input) {
  $(input).on({
  "focus": function (event) {
      $(event.target).select();
  },
  "keyup": function (event) {
      $(event.target).val(function (index, value ) {
          return value.replace(/\D/g, "")
                      .replace(/([0-9])([0-9]{3})$/, '$1.$2')
                      .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
      });
  }});
}

function formatText(data) {
  data = document.getElementsByClassName(data)
  var value
  for(let i = 0; i < data.length; i++) {
    value = data[i].innerText
    value = parseFloat(value).toLocaleString('es')
    data[i].innerText = value
  }
}

function formatInputLoaded(data) {
  data = document.getElementsByClassName(data)
  var value
  for(let i = 0; i < data.length; i++) {
    value = data[i].value
    value = parseFloat(value).toLocaleString('es')
    data[i].value = value
  }
}

function formatearFecha(msg) {
    let meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    let fecha = msg.split(' de ')

    if(fecha[0].length > 1) {
      var dia = fecha[0]
    } else {
      var dia = `0${fecha[0]}`
    }

    var mes = ''

    var anio = fecha[2]

    for(let i = 0; i < meses.length; i++) {
      if(meses[i] == fecha[1]) {
        if(i + 1 < 10) {
          mes = `0${i + 1}`
        } else {
          mes = `${i + 1}`
        }
      }
    }
    
    return `${anio}-${mes}-${dia}`
}

$(document).ready(function(){
 
  if(window.innerWidth < 768 && document.getElementsByTagName("form")){
      var botones = document.getElementsByClassName("btn")
      for(let i = 0; i < botones.length; i++) {
        botones[i].className += " btn-sm"
      }
  }

});