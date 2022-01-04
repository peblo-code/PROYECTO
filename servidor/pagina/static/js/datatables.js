function dataTable() {
    $(document).ready(function() {
        $('#tabla').DataTable({
            "language": {
                "emptyTable":     "La tabla se encuentra vacia.",
                "info":           "Mostrando _END_ de _MAX_ registros",
                "infoEmpty":      "",
                "infoFiltered":   "",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Mostrando _MENU_ registros por página",
                "loadingRecords": "Cargando...",
                "processing":     "Procesando...",
                "search":         "Buscar:",
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
}