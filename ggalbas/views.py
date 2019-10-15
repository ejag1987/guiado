import json
import random
import string
import datetime
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ggalbas.models import TblAlumnos, TblListas, TblPreguntausuarios, TblSubproducto, TblRegistroipAlumno, TblNiveles, TblInstituciones
from core.models import Preguntas2Basico, Pruebas


def index(request):
    captcha = random.randrange(1000, 9999)
    return render(request, 'ggalbas/login.html', {'captcha': captcha})


def nuevoAlumno(request):
    return render(request, 'ggalbas/nuevoAlumno.html')


def agregarAlumno(request):
    rut = request.POST['rut']
    nombres = request.POST['nombres'].upper()
    apellidos = request.POST['apellidos'].upper()
    pregunta = TblPreguntausuarios.objects.get(id_pregunta=int(request.POST['pregunta']))
    producto = TblSubproducto.objects.get(id_producto=2)
    answer = request.POST['respuesta'].upper()
    nivel = int(request.POST['curso'])
    letra = request.POST['letra'].upper()
    codigoLista = request.POST['codigoLista'].upper()
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(6))
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    fecha = request.POST['fecha']
    partes = fecha.split("T")[0].split("/")
    nacimiento = "-".join(reversed(partes))
    lista = TblListas.objects.get(codigo_lista=str(codigoLista))
    respuesta = {}

    ##se consulta si el rut ingresado pertenece a algun alumno
    consulta = TblAlumnos.objects.filter(rut_alumno=rut)

    if consulta:
        respuesta['alumno'] = 'alumno existe'
    else:
        ##se consulta que la lista este asociada al nivel
        consultaLista = TblListas.objects.filter(codigo_lista=codigoLista, id_nivel=nivel, letra=letra)
        if consultaLista:
            respuesta['lista'] = 'ok'
            ## consulta de cupos disponibles
            if consultaLista[0].total_alumnos == consultaLista[0].alumnos_registrados:
                respuesta['cupo'] = False
            else:
                try:
                    consultaLista.update(alumnos_registrados=int(consultaLista[0].alumnos_registrados) + 1)
                    respuesta['cupo'] = True
                except:
                    respuesta['status'] = 'error al guardar'
                registroAlumno = TblAlumnos(rut_alumno=rut, nombre=nombres, apellido=apellidos, clave=password,
                                            id_pregunta=pregunta, respuesta=answer, fecha_nacimiento=nacimiento,
                                            id_producto=producto, activo=1, nuevo=1, autonomo=0,
                                            fecha_registro=fechaActual, codigo_lista=lista)
                try:
                    registroAlumno.save()
                    respuesta['alumno'] = 'ok'
                    alumnoRegistrado = TblAlumnos.objects.filter(rut_alumno=rut)
                    respuesta['password'] = alumnoRegistrado[0].clave
                except:
                    respuesta['status'] = 'error al guardar'
        else:
            respuesta['lista'] = 'error'

    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def recuperaClave(request):
    return render(request, 'ggalbas/recuperaClave.html')


def verificaRut(request):
    rut = request.POST['rut']
    consulta = TblAlumnos.objects.filter(rut_alumno=rut)
    respuesta = {}
    if consulta:
        preguntaUser = TblPreguntausuarios.objects.filter(id_pregunta=int(str(consulta[0].id_pregunta)))
        if preguntaUser:
            respuesta['pregunta'] = preguntaUser[0].pregunta
            ##respuesta['respuesta'] = consulta[0].respuesta
            respuesta['status'] = 'consulta ok'
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def verificaRespuesta(request):
    rut = request.POST['rut']
    answer = request.POST['answer']
    consulta = TblAlumnos.objects.filter(rut_alumno=rut, respuesta=answer.upper())
    respuesta = {}
    if consulta:
        respuesta['status'] = 'respuesta ok'
        respuesta['password'] = consulta[0].clave
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def verificaRutIp(request):
    rut = request.POST['rut']
    ip = request.POST['ip']

    consulta = TblRegistroipAlumno.objects.filter(rut_alumno=rut, ip=ip)
    respuesta = {}
    if consulta:
        respuesta['status'] = 'validado'
        respuesta['rut'] = rut
    else:
        respuesta['status'] = 'sin datos'
        respuesta['formulario'] = '<div class="form-row"><div class="form-group col-12"><label for="inputPassword">Password</label><input type="password" class="form-control" id="password" placeholder="••••••••"></div></div>'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def ingresoCompleto(request):
    rut = request.POST['rut']
    password = request.POST['password']
    ip = request.POST['ip']
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    hoy = date.today()
    year = format(hoy.year)

    consulta = TblAlumnos.objects.filter(rut_alumno=rut, clave=password, activo=1, id_producto=2)
    respuesta = {}
    if consulta:
        registro = TblRegistroipAlumno(rut_alumno=TblAlumnos.objects.get(rut_alumno=rut), ip=ip,
                                       fecha_registro=fechaActual)
        try:
            registro.save()
            respuesta['status'] = 'datos alumno ok'
            ## Declaracion de las variables de session
            request.session['rut'] = consulta[0].rut_alumno
            request.session['nombres'] = consulta[0].nombre + ' ' + consulta[0].apellido
            listas = TblListas.objects.filter(codigo_lista=consulta[0].codigo_lista)
            nivel = str(listas[0].id_nivel)
            colegio = str(listas[0].rbd)
            niveles = TblNiveles.objects.filter(id_nivel=nivel)
            rbd = TblInstituciones.objects.filter(rbd=colegio)
            request.session['nivel'] = niveles[0].nivel + '-' + listas[0].letra
            request.session['rbd'] = rbd[0].nombre_institucion


            if consulta[0].nuevo == 1:
                respuesta['nuevo']= True
                prueba = 'P' + nivel + 'GG' + '01' + year
                request.session['prueba'] = prueba

            else:
                respuesta['diagnostico'] = 'No'
        except:
            respuesta['status'] = 'error de conexion'

    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def ingresoSoloRut(request):
    rut = request.POST['rut']
    hoy= date.today()
    year= format(hoy.year)

    consulta = TblAlumnos.objects.filter(rut_alumno=rut, activo=1, id_producto=2)
    respuesta = {}
    if consulta:
        respuesta['status'] = 'datos alumno ok'

        ## Declaracion de las variables de session
        request.session['rut'] = consulta[0].rut_alumno
        request.session['nombres'] = consulta[0].nombre + ' ' + consulta[0].apellido
        listas = TblListas.objects.filter(codigo_lista=consulta[0].codigo_lista)
        nivel = str(listas[0].id_nivel)
        colegio= str(listas[0].rbd)
        niveles = TblNiveles.objects.filter(id_nivel=nivel)
        rbd= TblInstituciones.objects.filter(rbd=colegio)
        request.session['nivel'] = niveles[0].nivel+'-'+listas[0].letra
        request.session['rbd'] = rbd[0].nombre_institucion


        if consulta[0].nuevo == 1:
           respuesta['nuevo']= True
           prueba = 'P'+ nivel +'GG'+'01'+year
           request.session['prueba'] = prueba
        else:
            respuesta['diagnostico'] = 'No'
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def antePortada(request):
    nombres= request.session['nombres']
    nivel = request.session['nivel']
    rbd = request.session['rbd']
    return render(request, 'ggalbas/antePortada.html', {'nombres': nombres, 'nivel': nivel, 'rbd': rbd})

def portadaVisor(request):
    prueba = request.session['prueba']
    consultaActividad = Pruebas.objects.using('e_test').filter(codprueba=prueba)
    if consultaActividad:
        ## se guarda en una variable de sesion el id de la prueba o guia que corresponda
        request.session['prueba_guia'] = consultaActividad[0].idprueba
        descripcion = consultaActividad[0].descprueba
    else:
        descripcion = 'no hay nada'

    return render(request, 'ggalbas/portadaVisor.html', {'prueba': prueba, 'descripcion': descripcion})

def visorActividades(request):
    pruebaGuia= request.session['prueba_guia']
    prueba = request.session['prueba']
    preguntas = Preguntas2Basico.objects.using('e_test').filter(idprueba=pruebaGuia)


    return render(request, 'ggalbas/visorActividades.html', {'prueba': prueba, 'pruebaGuia': pruebaGuia})
