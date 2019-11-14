$( document ).ready(function() {

 $('#recuperar-password').attr("disabled", true);

    $('#rut').blur(function(){
        verificaRut();
    });

    $('#validador').keyup(function(){
        verificaRut();
    });

	$('#recuperar-password').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var rutCompleto = $('#rut').val()+'-'+$('#validador').val();
        $('#errorRut').html('').fadeOut('fast');
        $('#errorRespuesta').html('').fadeOut('fast');
        $('#box-password-recuperada').fadeOut('fast');
        $('#forgot-password').html('');

          if ($('#rut').val().trim()=="" || $('#validador').val().trim()==""){
                $('#errorRespuesta').html('<span>rut o validador vacios</span>').fadeIn('fast');
          }
          else  if (Fn.validaRut(rutCompleto) == false){
             $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn('fast');
         }
         else if($('#respuesta-secreta').val().trim()==""){
              $('#errorRespuesta').html('<span>Debe ingresar una respuesta</span>').fadeIn('fast');
           }
            else{
            cargaAnimacion();
                $.ajax({
                        async: true,
                        type: "POST",
                        url: "recuperaClave/verificaRespuesta",
                        dataType: 'json',
                        data: {
                            rut: rutCompleto,
                            answer: $('#respuesta-secreta').val()
                          },
                        success: function(respuesta){
                             quitarAnimacion();
                            if (respuesta.status=='respuesta ok'){
                                $('#box-password-recuperada').fadeIn('fast');
                                $('#forgot-password').html('<span>'+respuesta.password+'</span>');
                            }
                            else{
                                $('#box-password-recuperada').fadeOut('fast');
                                $('#forgot-password').html('');
                                $('#errorRespuesta').html('<span>Respuesta inválida</span>').fadeIn('fast');
                            }
                          },

                });
            }
	});
});

 function cargaAnimacion(){
  $('#loader').fadeIn('fast');
 }

function quitarAnimacion(){
  $('#loader').fadeOut('fast');
 }


  var Fn = {
  // Valida el rut con su cadena completa "XXXXXXXX-X"
  validaRut : function (rutCompleto) {
    rutCompleto = rutCompleto.replace("‐","-");
    if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test( rutCompleto ))
      return false;
    var tmp   = rutCompleto.split('-');
    var digv  = tmp[1];
    var rut   = tmp[0];
    if ( digv == 'K' ) digv = 'k' ;

    return (Fn.dv(rut) == digv );
  },
  dv : function(T){
    var M=0,S=1;
    for(;T;T=Math.floor(T/10))
      S=(S+T%10*(9-M++%6))%11;
    return S?S-1:'k';
  }
}


function verificaRut(){

    $('#errorRut').html('').fadeOut('fast');
    $('#errorRespuesta').html('').fadeOut('fast');
	$('#div-pregunta').fadeOut('fast');
    $('#label-pregunta').html('');
    $('#div-respuesta').fadeOut('fast');
    $('#respuesta-secreta').val('');
    $('#box-password-recuperada').fadeOut('fast');
    $('#forgot-password').html('');
    $('#recuperar-password').attr("disabled", true);

    var rutCompleto = $('#rut').val().trim()+'-'+$('#validador').val().trim();

      if ($('#rut').val().trim()=="" || $('#validador').val().trim()==""){
            console.log('rut o validador vacios');
      }
      else  if (Fn.validaRut(rutCompleto) == false){
         $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn('fast');
     }
      else {
              cargaAnimacion();

                $.ajax({
                  async: true,
                  type: "POST",
                  url: "recuperaClave/verificaRut",
                  dataType: 'json',
                  data: {
                    rut: rutCompleto
                  },
                  success: function(data){
                    quitarAnimacion();
                  	if(data.status=='consulta ok'){
                  		$('#recuperar-password').removeAttr("disabled");
                  		$('#div-pregunta').fadeIn('fast');
                  		$('#label-pregunta').html(data.pregunta);
                  		$('#div-respuesta').fadeIn('fast');
                  		$('#respuesta-secreta').val('');
                  	}
                  	else{
                  		$('#errorRut').html('<span>Rut no se encuentra registrado</span>').fadeIn('fast');
                  	}
                  },
                  error: function(){
                    console.log('error del sistema');
                  }
                });
            }

}


