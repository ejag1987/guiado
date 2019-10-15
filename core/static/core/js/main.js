$(document).ready(function(){
  // Solo numeros en campo
  $('.input-number').on('input', function () { 
    this.value = this.value.replace(/[^0-9]/g,'');
  });
  
});