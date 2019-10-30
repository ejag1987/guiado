  var url = jQuery(location).attr('href');

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

 validaForm();


function validaForm(){

  $('#registro').on('click', function(){

      if ($('#rut').val() =="" || $('#validador').val()==""){
            $('#textoErrorModal').html('Para registrarse ingrese su RUT');
            $('#modalError').modal("show");
       }
       else if (Fn.validaRut($('#rut').val()+'-'+$('#validador').val())==false){
          $('#textoErrorModal').html('Debe ingresar un Rut válido');
          $('#modalError').modal("show");
       }
       else if (($('#curso').val()=="") || ($('#letra').val()=="")){
          $('#textoErrorModal').html('Para registrarse complete su curso');
          $('#modalError').modal("show");
       }
       else if($('#codigo-lista').val().trim()==""){
            $('#textoErrorModal').html('Para registrarse ingrese el código de lista');
            $('#modalError').modal("show");
       }
        else if($('#nombres').val().trim()=="" || $("#nombres").val().trim().length < 3 ){
           $('#textoErrorModal').html('Para registrarse ingrese sus nombres');
           $('#modalError').modal("show");
       }
        else if($('#apellidos').val().trim()=="" || $("#apellidos").val().trim().length < 3){
           $('#textoErrorModal').html('Para registrarse ingrese sus apellidos');
           $('#modalError').modal("show");
       }
       else if($('#pregunta').val()==""){
           $('#textoErrorModal').html('Para registrarse seleccione una pregunta de seguridad');
           $('#modalError').modal("show");
       }
       else if($('#respuesta').val().trim()==""){
            $('#textoErrorModal').html('Para registrarse escriba la respuesta a la pregunta de seguridad');
            $('#modalError').modal("show");
          }
          else{

          $.ajax({
                  async: true,
                  type: "POST",
                  url: url+"/agregarAlumno",
                  dataType: 'json',
                  data: {   rut: $('#rut').val()+'-'+$('#validador').val(),
                            curso: $('#curso').val(),
                            letra: $('#letra').val(),
                            codigoLista: $('#codigo-lista').val(),
                            nombres: $('#nombres').val(),
                            apellidos: $('#apellidos').val(),
                            pregunta: $('#pregunta').val(),
                            respuesta: $('#respuesta').val()
                          },
                  success: function(respuesta){
                        if(respuesta.alumno=='alumno existe'){
                          $('#textoErrorModal').html('El rut ingresado ya se encuentra registrado');
                          $('#modalError').modal("show");
                        }
                        else  if(respuesta.lista=='error'){
                          $('#textoErrorModal').html('El código de lista no es válido para el curso y letra ingresados');
                          $('#modalError').modal("show");
                        }
                        else if(!respuesta.cupo){
                          $('#textoErrorModal').html('no hay cupo');
                          $('#modalError').modal("show");
                        }
                        else{
                           $('#textoOkModal').html(respuesta.password);
                            $('#modalOk').modal("show");
                           regresaIndex();
                        }
                      },
                  error: function(){
                     $('#modalError').modal("show");
                     $('#textoErrorModal').html('Error al Registrar al Alumno');
                  }
                });
        }
  });
}

function regresaIndex(){
  $('#aceptar').on('click', function(){
    var url = getAbsolutePath();
   // console.log(url);
  $(location).attr('href',url);
  });
}

function getAbsolutePath() {
    var loc = window.location;
    var pathName = loc.pathname.substring(0, loc.pathname.lastIndexOf('/') + 1);
    return loc.href.substring(0, loc.href.length - ((loc.pathname + loc.search + loc.hash).length - pathName.length));
}
