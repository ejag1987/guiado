var url;
$('#continuar').on('click', function(){
    url = "portadaVisor";
    $(location).attr('href',url);
});
$('#vuelveAnteP').on('click', function(){
    url = 'antePortada';
    $(location).attr('href',url);
});

