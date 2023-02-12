var tabla_categorias;

$(function () {
    tabla_categorias = $('#data').DataTable({
        responsive:true,
        autoWidth:false,
        destroy:true,
        deferRender: true,
        ajax:{
            url:window.location.pathname,
            type:'POST',
            data:{
                'action':'ver_categorias'
            },
            dataSrc:''
        },
        columns:[
            {'data':'nombre'},
            {'data':'descripcion'},
            {'data':'imagen'},
            {'data':'buttons'}
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
            {
                targets : [-2],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<img src="'+ row.imagen +'"  class="img-fluid mx-auto d-block" style="width:50px; height:35px">';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tabla_categorias.cell($(this).closest('td , li')).index();
        var data = tabla_categorias.row(tr.row).data();
        var parametros = new FormData();
        parametros.append('action', 'delete');
        parametros.append('id', data.id)
        actions_switalert_ajax(window.location.pathname, 'Notificación', '¿Desea eliminar el siguiente registro?', parametros, function () {
            location.href = window.location.pathname;
        });
    });
});