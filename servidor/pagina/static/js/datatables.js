function dataTable() {
    $(document).ready(function() {
        $('#tabla').DataTable({
            responsive: true,
            "language": {
                "emptyTable":     "La tabla se encuentra vacia.",
                "info":           "Mostrando _END_ de _MAX_ registros",
                "infoEmpty":      "",
                "infoFiltered":   "",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Mostrar _MENU_ registros",
                "loadingRecords": "Cargando...",
                "processing":     "Procesando...",
                "search":         "",
                "zeroRecords":    "No se obtuvo ninguna coincidencia",
                oPaginate: {
                    sNext: '<i class="fa fa-forward"></i>',
                    sPrevious: '<i class="fa fa-backward"></i>',
                    sFirst: '<i class="fa fa-step-backward"></i>',
                    sLast: '<i class="fa fa-step-forward"></i>'
                }
            }
        });
    });
    document.getElementById('tabla').style = "padding-top: 1em"
}

function dataTableId(tabla) {
    $(document).ready(function() {
        $(`#${tabla}`).DataTable({
            "language": {
                "emptyTable":     "La tabla se encuentra vacia.",
                "info":           "Mostrando _END_ de _MAX_ registros",
                "infoEmpty":      "",
                "infoFiltered":   "",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Mostrar _MENU_ registros",
                "loadingRecords": "Cargando...",
                "processing":     "Procesando...",
                "search":         "",
                "zeroRecords":    "No se obtuvo ninguna coincidencia",
                oPaginate: {
                    sNext: '<i class="fa fa-forward"></i>',
                    sPrevious: '<i class="fa fa-backward"></i>',
                    sFirst: '<i class="fa fa-step-backward"></i>',
                    sLast: '<i class="fa fa-step-forward"></i>'
                }
            }
        });
    });
    document.getElementById(tabla).style = "padding-top: 1em"
}