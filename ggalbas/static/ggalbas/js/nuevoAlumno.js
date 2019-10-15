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
$(function(){
$('#fecha').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'dd/mm/yy',
    firstDay: 1,
    maxDate: '+od'

});
});
validaForm();


function validaForm(){
  var rut, validador, curso, letra, lista, nombres, apellidos, pregunta, respuesta;
  $('#registro').on('click', function(){
  rut = $('#rut').val();
  validador =  $('#validador').val();
  curso = $('#curso').val();
  letra = $('#letra').val();
  lista = $('#codigo-lista').val();
  nombres = $('#nombres').val();
  apellidos = $('#apellidos').val();
  pregunta = $('#pregunta').val();
  fecha = $('#fecha').val();
  respuesta = $('#respuesta').val();

  if ((rut=="") || (validador=="")){
    $('#error').html('<span>Debe colocar su rut para registrarse</span>').fadeIn(1000);
      }
  else{
      $('#error').html('');
      var rutValidado = Fn.validaRut(rut+'-'+validador);
      if(rutValidado == false){
        $('#error').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
     }
      else{
        $('#error').html('');
        if ((curso=="") || (letra=="")){
        $('#error').html('<span>Debe seleccionar su curso</span>').fadeIn(1000);
        }
        else{
        $('#error').html('');
          if(lista==""){
          $('#error').html('<span>Debe ingresar el código lista</span>').fadeIn(1000);
          }
          else{
          $('#error').html('');
          if (fecha ==''){
            $('#error').html('<span>Debe colocar su fecha de nacimiento</span>').fadeIn(1000);
          }
          else{
          $('#error').html('');
          if(pregunta==""){
            $('#error').html('<span>Debe elegir una pregunta</span>').fadeIn(1000);
          }
          else{
          $('#error').html('');
          if(respuesta==""){
            $('#error').html('<span>Debe ingresar una respuesta</span>').fadeIn(1000);
          }
          else{
          $('#error').html('');
          var parametros= { rut:rut+'-'+validador, 
                            curso: curso, 
                            letra: letra, 
                            codigoLista: lista, 
                            nombres: nombres, 
                            apellidos: apellidos,
                            fecha: fecha,
                            pregunta: pregunta, 
                            respuesta: respuesta
                          };
          $.ajax({
                  async: true,
                  type: "POST",
                  url: url+"/agregarAlumno",
                  dataType: 'json',
                  data: parametros,
                  success: function(respuesta){
                    console.log(respuesta);
                    if(respuesta.alumno=='alumno existe'){
                      $('#modalError').modal("show");
                      $('#textoErrorModal').html('El rut ingresado ya se encuentra registrado'); 
                    }
                    else{
                      $('#textoErrorModal').html('');
                      if(respuesta.lista=='error'){
                        $('#modalError').modal("show");
                      $('#textoErrorModal').html('Codigo lista incorrecto');
                      }
                      else{
                        $('#textoErrorModal').html('');
                        if(!respuesta.cupo){
                          $('#modalError').modal("show");
                          $('#textoErrorModal').html('no hay cupo');

                        }
                        else{ 
                         $('#modalOk').modal("show");
                         $('#textoOkModal').html(respuesta.password);
                         regresaIndex();
                        

                        }
                        
                      }
                      
                    }


                  },
                  error: function(){
                    console.log('error del sistema');
                     $('#modalError').modal("show");
                      $('#textoErrorModal').html('Error al Registrar al Alumno');
                  }
                });
           }
          }
         }
         }
        }
      }
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