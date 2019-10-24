var url;

$('#continuar').on('click', function(){
    url = "portadaVisor";
    $(location).attr('href',url);
});

$('#vuelveAnteP').on('click', function(){
    url = 'antePortada';
    $(location).attr('href',url);
});


function evaluaEjercicio(){

    $('#flecha').on('click', function(){

        var respuestaAlumno = '';
        var abecedario=new Array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

        var continuar=1;
        var selecciona_check=0;
        var selecciona_radio=0;

        if ($('.fill-input').length) { // los campos son de tipo text
            
            $(".fill-input").each(function (index) {  
                if($(this).val()==''){
                    continuar = 0;
                    $('#ModalEjercicio').modal('show');
                    return false;
                }
                respuestaAlumno += respuestaAlumno == '' ? $(this).val() : ","+$(this).val();
            });
        }

        if ($('.radio-input').length) { // los campos son de tipo radio
           
            $(".radio-input").each(function (index) {             
                if($(this).is(':checked')) {  
                    selecciona_radio =1;
                    respuestaAlumno += abecedario[parseInt($(this).attr('id')) -1];
                }          
            });

            if(selecciona_radio==0){
                continuar = 0;
                $('#ModalEjercicio').modal('show');
            }
        }

        if ($('.checkbox-input').length) { // los campos son de tipo checkbox

            $(".checkbox-input").each(function (index) {             
                if($(this).is(':checked')) {  
                    selecciona_check =1; 
                    respuestaAlumno += abecedario[parseInt($(this).attr('id')) -1];
                }         
            });
        
            if(selecciona_check==0){
                continuar = 0;
                $('#ModalEjercicio').modal('show');
            }
        }
 
        if (continuar==1){

            $.ajax({
                async: true,
                type: "POST",
                url: "guardaRespuesta",
                dataType: 'json',
                data: { 'respuestaAlumno': respuestaAlumno },
                success:function(respuesta){
                    if (respuesta.alumnoRespuesta){
                        url = 'visorActividades';
                        $(location).attr('href',url);
                    }
                    else{
                    console.log ('aqui va el modal de error');
                    }

                   console.log(respuesta.alumnoRespuesta);
                }

            });
        }
        
    });

}

evaluaEjercicio();
