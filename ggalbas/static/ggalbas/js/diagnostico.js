var url;
$('#continuar').on('click', function(){
    url = "portadaVisor";
    $(location).attr('href',url);
});
$('#vuelveAnteP').on('click', function(){
    url = 'antePortada';
    $(location).attr('href',url);
});

evaluaEjercicio();

function evaluaEjercicio(){

$('#flecha').on('click', function(){
    fill1= $('#fill-1').val();

    if(fill1==""){
        $('#ModalEjercicio').modal('show');
    }
    else {
        $.ajax({
            async: true,
            type: "POST",
            url: "guardaRespuesta",
            dataType: 'json',
            data: {
                    fill1: fill1,
                  },
            success:function(respuesta){
                console.log(respuesta);
            }

        });
    }
});

}


