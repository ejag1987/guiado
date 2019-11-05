$('#entrar').attr("disabled", true);
var url = jQuery(location).attr('href');

 function cargaAnimacion(){
  $('#loader').html('<img src="/static/ggalbas/images/loader.gif" alt="loader">').fadeOut(1000);
  return true;
 }
 function mostrarPassword(){
$('#input-password').removeClass('oculto');
 }
 function quitarPassword(){
  $('#input-password').addClass('oculto');
 }
 function mostrarCaptcha(){
  $('#captcha').removeClass('oculto');
  $('#captcha').css('display', 'flex');

 }
 function desactivarCaptcha(){
  $('#captcha').addClass('oculto');
 }
 function validaIngresoRut(){
  $('#entrar').on('click', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
            async: true,
            type: 'POST',
            url: url+"ingresoSoloRut",
            dataType: 'json',
            data: {
                    rut: $('#rut').val()+-+$('#validador').val() 
            },
            success: function (respuesta){
             console.log(respuesta);
              //console.log('estoy aqui');
              if(respuesta.status=='datos alumno ok'){
                if (respuesta.nuevo){
                    var url = "antePortada";
                    $(location).attr('href',url);
                }

               console.log(respuesta.nombreCompleto)

              }


            }

    });
  });
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

function validaIngresoCompleto(ip){
console.log(ip);
$('#entrar').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var rut= $('#rut').val();
    var validador= $('#validador').val();
    var validacion = Fn.validaRut(rut+'-'+validador);

    if (rut=="" || validador=="" ){
   // $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000); 
    }
    else{
       $('#errorRut').fadeOut('slow');
       if ($('#password').val()==""){
        $('#errorPass').html('<span> Debe ingresar su contraseña</span>').fadeIn(1000);
        console.log('sin password');
        }
        else{
          $('#errorPass').fadeOut('slow');
          if($('#img-captcha').text()!=$('#texto-captcha').val() || $('#texto-captcha').val()=="" ){
            $('#errorCaptcha').html('<span>Ingrese los números del recuadro naranjo</span>').fadeIn(1000);
            console.log('captcha diferente');
          }
          else{
            $.ajax({
            async: true,
            type: 'POST',
            url: url+"ingresoCompleto",
            dataType: 'json',
            data: {
                    rut: $('#rut').val()+-+$('#validador').val(),
                     password: $('#password').val(),
                     ip: ip
            },
            success: function (respuesta){
              $('#errorPass').fadeOut('slow');
              $('#errorCaptcha').fadeOut('slow');

              console.log(respuesta);
              if(respuesta.status=='datos alumno ok'){
                console.log(respuesta.nivelacion)
                if(respuesta.status=='datos alumno ok'){
                if (respuesta.nuevo){
                    var url = "antePortada";
                    $(location).attr('href',url);
                }

              }
              }
              else{
                console.log(respuesta.status);

                 $('#errorPass').html('<span>El rut y/o contraseña ingresados no son válidos</span>').fadeIn(1000);
              }

            }
          });
          }
        }
    }
    });
}

validaRutIp();

function validaRutIp(){

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

        cargaAnimacion();

            if (rutValidado == false){

              $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);

              quitarPassword();

              desactivarCaptcha();
               
            }
            else {

             cargaAnimacion();

             $('#errorRut').fadeOut('slow');

             $.getJSON( "http://jsonip.com?callback=?", function(data) {
                verificaRutIp(rutCompleto,data.ip)
             })
             .fail(function() {
                $.ajax( "obtenerIp" )
                      .done(function(ip) {
                       verificaRutIp(rutCompleto,ip)
                      });
             });

            } 
      }
    });
  });
}

function verificaRutIp(rut,ip){

$.ajax({
      async: true,
      type: "POST",
      url: url+"verificaRutIp",
      dataType: 'json',
      data: {
        'ip': ip,
        'rut': rut
      },
      success: function(respuesta){

        cargaAnimacion();

        console.log(respuesta);

        $('#entrar').removeAttr("disabled");

        if(respuesta.status=='validado'){

              quitarPassword();

              desactivarCaptcha();

              $('#input-password').html('');

              validaIngresoRut();

        }
        else{

              console.log('no validado');

              mostrarPassword();

              $('#input-password').html(respuesta.formulario);

              mostrarCaptcha();

              validaIngresoCompleto(ip);

        }
      },
      error: function(){
        console.log('hay un error');
      }
    });

}

