var url;
var respuestaAlumno;

$( document ).ready(function() {

    $('#continuar').on('click', function(){
        url = 'portadaVisor';
        $(location).attr('href',url);
    });

    $('#vuelveAnteP').on('click', function(){
        url = 'antePortada';
        $(location).attr('href',url);
    });

});

function proximoEjercicio(){

        var abecedario=new Array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

        var continuar=1;

        var valor = '';

        respuestaAlumno = '';

        if ($('.fill-input').length) { // los campos son de tipo text
            $(".fill-input").each(function (index) {
                if($(this).val().trim()==''){
                    valor= 'null';
                    continuar = 0;
                }else{
                    valor = $(this).val();
                }
                respuestaAlumno += respuestaAlumno == '' ? valor : ","+valor;
            });
        }


        if ($('.radio-check').length) { // los campos son de tipo radio o de tipo checkbox.
            $(".radio-check").each(function (index) {
                if($(this).is(':checked')) {
                    respuestaAlumno += abecedario[parseInt($(this).attr('id')) -1];
                }          
            });

            if(respuestaAlumno == ''){
                continuar = 0;
            }
        }

          if(continuar==0){
                $('#ModalConfirmacion').modal('show');
            }else{
                guardaRespuesta();
            }

}

function guardaRespuesta(){

            $.ajax({
                async: true,
                type: "POST",
                url: "guardaRespuesta",
                dataType: 'json',
                data: { 'respuestaAlumno': respuestaAlumno },
                success:function(respuesta){
                    if (respuesta.fin){
                        $(location).attr('href','resultadoDiagnostico');
                    }
                    else if (respuesta.alumnoRespuesta){
                         $(location).attr('href','visorActividades');
                    } else{
                        console.log ('aqui va el modal de error');
                    }
                }
            });
}

function playrecord(){
    document.getElementById('player').pause();
    document.getElementById('player').currentTime = 0;
    document.getElementById('player').play();
}
