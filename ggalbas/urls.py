from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recuperaClave', views.recuperaClave, name='recuperaClave'),
    path('nuevoAlumno', views.nuevoAlumno, name='nuevoAlumno'),
    path('nuevoAlumno/agregarAlumno', views.agregarAlumno, name='agregarAlumno'),
    path('recuperaClave/verificaRut', views.verificaRut, name='verificaRut'),
    path('recuperaClave/verificaRespuesta', views.verificaRespuesta, name='verificaRespuesta'),
    path('verificaRutIp', views.verificaRutIp, name='verificaRutIp'),
    path('ingresoCompleto', views.ingresoCompleto, name='ingresoCompleto'),
    path('ingresoSoloRut', views.ingresoSoloRut, name='ingresoSoloRut'),
    path('antePortada', views.antePortada, name='antePortada'),
    path('portadaVisor', views.portadaVisor, name='portadaVisor'),
    path('visorActividades', views.visorActividades, name='visorActividades'),
]