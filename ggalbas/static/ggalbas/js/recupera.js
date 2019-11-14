 $('#recuperar-password').attr("disabled", true);
 var url = jQuery(location).attr('href');
 
 function cargaAnimacion(){
  $('#loader').html('<img src="../static/images/loader.gif" alt="loader">').fadeOut('slow');
  return true;
 }

 function reset(){
	$('#recuperar-password').attr("disabled", true);
    $('#pregunta-secreta').html('');
    $('#label-respuesta').html('');
    $('#respuesta').html('');
    $('#errorRespuesta').html('');
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

consultaRut();

function consultaRut(){
	  $('#rut').on('blur', function(){
    var rut = $(this).val();
    $('#validador').keyup(function(){
      var validador= $(this).val();
      var rutCompleto = rut+'-'+validador;
      if (rut=="" || validador==""){
        console.log('rut o validador vacios');
      }
      else{
        var rutValidado = Fn.validaRut(rutCompleto);
            

            if (rutValidado == false){
              cargaAnimacion();
              $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
            }
            else {
              cargaAnimacion();
              $('#errorRut').fadeOut('slow');
                $.ajax({
                  async: true,
                  type: "POST",
                  url: url+"/verificaRut",
                  dataType: 'json',
                  data: {
                    rut: rutCompleto
                  },
                  success: function(respuesta){
                  	if(respuesta.status=='consulta ok'){
                  		$('#recuperar-password').removeAttr("disabled");
                  		$('#pregunta-secreta').html('<label id="pregunta-secreta" for="alumnonuevo-apoderado" class=" col-form-label">'+respuesta.pregunta+'</label>');
                  		$('#label-respuesta').html('<label for="respuesta-seguridad" class="col-form-label">Respuesta: </label>');
                  		$('#respuesta').html('<input type="text" class="form-control input-respuesta">');
                  		recuperaPass();
                  	}
                  	else{
                  		$('#errorRut').html('<span>Rut no se encuentra registrado</span>').fadeIn(1000);
                  		reset();
                  	}

                  },
                  error: function(){
                    console.log(respuesta);
                    console.log('error del sistema');
                  }
                });
            } 
      }
    });
  });
}

function recuperaPass(){
	$('#recuperar-password').on('click', function(e){
	e.preventDefault();
    e.stopImmediatePropagation();

    var rutCompleto = $('#rut').val()+'-'+$('#validador').val();

    if($('.input-respuesta').val()==""){
    	$('#errorRespuesta').html('<span>Debe ingresar una respuesta</span>').fadeIn(1000);
    }
    else{
    	$('#errorRespuesta').fadeOut('slow');
    	$.ajax({
    	        async: true,
                type: "POST",
                url: url+"/verificaRespuesta",
                dataType: 'json',
                data: {
                    rut: rutCompleto,
                    answer: $('.input-respuesta').val()
                  },
                success: function(respuesta){
                  	console.log(respuesta);
                  	if (respuesta.status=='respuesta ok'){
                  		$('#errorRespuesta').html('');
                  		$('#box-password-recuperada').removeClass('d-none');
                  		$('#forgot-password').html('<span>'+respuesta.password+'</span>');
                  	}
                  	else{
                  		$('#box-password-recuperada').addClass('d-none');
                  		$('#forgot-password').html('');
                  		$('#errorRespuesta').html('<span>Respuesta inválida</span>').fadeIn(1000);
                  	}
                  },

    	});
    }

	});
}

