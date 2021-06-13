function listadoUsuarios(){
    $.ajax({
        url: "/listar_usuarios/",
        type: "get",
        dataType: "json",
        success: function(response){
            $('nombretabla_usuarios tbody').html("");
            for(let i = 0; i < response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i +1) + '</td>';
                fila += '<td>' + response[i]["fields"]['nombre'] + '</td>';
                fila += '<td>' + response[i]["fields"]['apellido'] + '</td>';
                fila += '<td>' + response[i]["fields"]['rut'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fecha nacimiento'] + '</td>';
                fila += '<td>' + response[i]["fields"]['motivo atencion'] + '</td>';
                fila += '<td>' + response[i]["fields"]['email'] + '</td>';
                fila += '<td>' + response[i]["fields"]['direccion'] + '</td>';
                fila += '<td><button>Modificar</button><button>Eliminar</button></td>';

                fila += '</tr>';
            }
            $('#tabla_usuarios').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de _MAX_ total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                      first: "Primero",
                      last: "Ultimo",
                      next: "Siguiente",
                      previous: "Anterior",
                    },
                  },
            });
        },    
        error: function(error){
            console.log(error);

        }

        
    });
}

$(document).ready(function (){
    listadoUsuarios();
});
