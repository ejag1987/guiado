import json
import random
import string
import datetime
import base64
import socket
from datetime import date
import math
from django.http import HttpResponse
from django.shortcuts import render

from ggalbas.models import TblAlumnos, TblListas, TblPreguntausuarios, TblSubproducto, TblRegistroipAlumno, TblNiveles, \
    TblInstituciones, TblActividades, TblTipoActividad, TblAlumnoActividades, TblAlumnoRespuestas, TblPreguntas, \
    TblHabilidades, TblEje, TblAlumnoDiagnostico, TblContenidoUnidad, TblUnidades
from core.models import Preguntas2Basico, Pruebas, PreguntasInstancias


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
                                            id_pregunta=pregunta, respuesta=answer,
                                            id_producto=producto, activo=1, nuevo=1, autonomo=0,
                                            fecha_registro=fechaActual,
                                            codigo_lista=TblListas.objects.get(codigo_lista=str(codigoLista)))
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
    respuesta = {}

    consulta = TblRegistroipAlumno.objects.filter(rut_alumno=rut, ip=ip)

    if consulta:
        respuesta['status'] = 'validado'
    else:
        respuesta['status'] = 'sin datos'

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
            # Declaracion de las variables de session
            request.session['rut'] = consulta[0].rut_alumno
            request.session['nombres'] = consulta[0].nombre + ' ' + consulta[0].apellido
            listas = TblListas.objects.filter(codigo_lista=consulta[0].codigo_lista)
            nivel = str(listas[0].id_nivel)
            colegio = str(listas[0].rbd)
            niveles = TblNiveles.objects.filter(id_nivel=nivel)
            rbd = TblInstituciones.objects.filter(rbd=colegio)
            request.session['nivel'] = niveles[0].nivel + '-' + listas[0].letra
            request.session['id_nivel'] = nivel
            request.session['rbd'] = rbd[0].nombre_institucion

            if consulta[0].nuevo == 1:
                respuesta['nuevo'] = True
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
    hoy = date.today()
    year = format(hoy.year)

    consulta = TblAlumnos.objects.filter(rut_alumno=rut, activo=1, id_producto=2)
    respuesta = {}
    if consulta:
        respuesta['status'] = 'datos alumno ok'

        # Declaracion de las variables de session
        request.session['rut'] = consulta[0].rut_alumno
        request.session['nombres'] = consulta[0].nombre + ' ' + consulta[0].apellido
        listas = TblListas.objects.filter(codigo_lista=consulta[0].codigo_lista)
        nivel = str(listas[0].id_nivel)
        colegio = str(listas[0].rbd)
        niveles = TblNiveles.objects.filter(id_nivel=nivel)
        rbd = TblInstituciones.objects.filter(rbd=colegio)
        request.session['id_nivel'] = nivel
        request.session['nivel'] = niveles[0].nivel + '-' + listas[0].letra
        request.session['rbd'] = rbd[0].nombre_institucion

        if consulta[0].nuevo == 1:
            respuesta['nuevo'] = True
            prueba = 'P' + nivel + 'GG' + '01' + year
            request.session['prueba'] = prueba
        else:
            # Se debe consultar en tbl_actividades para saber en que actividad se encuentra
            respuesta['diagnostico'] = 'No'
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def antePortada(request):

    if 3 <= int(request.session['id_nivel']) <= 5:
        personajes_a = 'basica3-5_a.png'
        personajes_b = 'basica3-5_b.png'
    elif 6 <= int(request.session['id_nivel']) <= 8:
        personajes_a = 'basica6-8_a.png'
        personajes_b = 'basica6-8_b.png'

    data = {'nombres': request.session['nombres'],
            'nivel': request.session['nivel'],
            'rbd': request.session['rbd'],
            'personajes_a': personajes_a,
            'personajes_b': personajes_b
            }
    return render(request, 'ggalbas/antePortada.html', data)


def portadaVisor(request):
    prueba = request.session['prueba']
    consultaActividad = Pruebas.objects.using('e_test').filter(codprueba=prueba)
    if consultaActividad:
        # # se guarda en una variable de sesion el id de la prueba o guia que corresponda
        request.session['prueba_guia'] = consultaActividad[0].idprueba
        descripcion = consultaActividad[0].descprueba
    else:
        descripcion = 'no hay nada'

    if 3 <= int(request.session['id_nivel']) <= 5:
        personajes_a = 'Diag-PInicial-basica345-1.png'
        personajes_b = 'Diag-PInicial-basica345-2.png'
    elif 6 <= int(request.session['id_nivel']) <= 8:
        personajes_a = 'Diag-PInicial-basica678-1.png'
        personajes_b = 'Diag-PInicial-basica678-2.png'

    data = {'prueba': prueba,
            'descripcion': descripcion,
            'personajes_a': personajes_a,
            'personajes_b': personajes_b
           }
    return render(request, 'ggalbas/portadaVisor.html', data)


def visorActividades(request):
    pruebaGuia = request.session['prueba_guia']
    prueba = request.session['prueba']
    actividad = TblActividades.objects.filter(prueba_guia=pruebaGuia)
    rutAlumno = request.session['rut']
    hoy = date.today()
    year = format(hoy.year)
    id_nivel = request.session['id_nivel']

    if actividad:
        descripcion = actividad[0].descripcion_actividades
    else:
        datosPruebas = Pruebas.objects.using('e_test').filter(codprueba=prueba, idprueba=pruebaGuia)
        if datosPruebas:
            actividades = TblActividades(nombre_actividad=prueba, descripcion_actividades=datosPruebas[0].descprueba,
                                         id_tipo_actividad=TblTipoActividad.objects.get(id_tipo_actividad=1),
                                         npreguntas=datosPruebas[0].npreguntas, prueba_guia=pruebaGuia)
            try:
                actividades.save()
            except:
                print('no se guardo')
            descripcion = 'sin'
        else:
            descripcion = 'no hay actividad'

    preguntas = Preguntas2Basico.objects.using('e_test').filter(idprueba=pruebaGuia)
    total_ejercicios = preguntas.count()
    respuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=rutAlumno, prueba_guia=pruebaGuia)

    if respuestas:
        npregunta = int(respuestas.last().npregunta)
    else:
        npregunta = 0

    img = base64.b64encode(preguntas[npregunta].imagen).decode()
    posiciones = str(preguntas[npregunta].posiciones_botones)
    pos_boton = posiciones.replace('!', "")
    lista_pos = pos_boton.split(',')
    posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
    npreg = preguntas[npregunta].npregunta
    tipoEjercicio = preguntas[npregunta].tipo_ejercicio
    audio_ejercicio = 'P' + str(id_nivel) + 'GG01' + str(year) + '_e' + str(npreg)+'_int.ogg'

    if 3 <= int(id_nivel) <= 4:
        ver_audio = True
    elif 5 <= int(id_nivel) <= 8:
        ver_audio = False

    data = {
        'title': 'imagen-ejercicio',
        'img': img,
        'prueba': prueba,
        'descripcion': descripcion,
        'botones': posicion_boton,
        'nejercicio': npreg,
        'tipoE': tipoEjercicio,
        'audio_ejercicio': audio_ejercicio,
        'ver_audio': ver_audio,
        'total_ejercicios': total_ejercicios
    }

    return render(request, 'ggalbas/visorActividades.html', data)


def guardaRespuesta(request):
    parametros = request.POST['respuestaAlumno']
    respuestaAlumno = parametros.split(sep=',')
    pruebaGuia = request.session['prueba_guia']
    rutAlumno = request.session['rut']
    respuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=rutAlumno, prueba_guia=pruebaGuia)
    totalPreg = Pruebas.objects.using('e_test').filter(idprueba=pruebaGuia)
    respuesta = {}

    if respuestas:
        npregunta = int(respuestas.last().npregunta) + 1
    else:
        npregunta = 1

    respuestaActividad = PreguntasInstancias.objects.using('e_test').filter(idprueba=pruebaGuia, npregunta=npregunta)
    preguntas = Preguntas2Basico.objects.using('e_test').filter(idprueba=pruebaGuia, npregunta=npregunta)
    correcta = respuestaActividad[0].respuesta_pregunta
    cantidad = int(preguntas[0].num_campos_completar)
    tipoE = preguntas[0].tipo_ejercicio
    instancias = 0

    if tipoE == 1:
        respCorrecta = correcta.replace('~', ",")
        listaRespuestas = respCorrecta.split(sep=',')
        for x in range(cantidad):
            if listaRespuestas[x] == respuestaAlumno[x]:
                instancias += 1
        instancia = int(instancias) / cantidad
    elif tipoE == 3:
        respCorrecta = correcta.replace('~', ",")
        listaRespuestas = respCorrecta.split(sep=',')
        if listaRespuestas[0] == respuestaAlumno[0]:
            instancia = 1
        else:
            instancia = 0

    else:
        listaRespuestas = correcta.split(sep=',')
        if listaRespuestas == respuestaAlumno:
            instancia = 1
        else:
            instancia = 0

    registroRespuesta = TblAlumnoRespuestas(rut_alumno=TblAlumnos.objects.get(rut_alumno=rutAlumno),
                                            npregunta=npregunta, prueba_guia=pruebaGuia,
                                            respuesta_alumno=respuestaAlumno, aprobada=instancia)
    try:
        registroRespuesta.save()
        respuesta['alumnoRespuesta'] = True
    except:
        respuesta['alumnoRespuesta'] = False

    if int(totalPreg[0].npreguntas) == int(registroRespuesta.npregunta):
        respuesta['fin'] = True
    else:
        respuesta['fin'] = False

    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def resultadoDiagnostico(request):
    pruebaGuia = request.session['prueba_guia']
    prueba = request.session['prueba']
    rut = request.session['rut']
    nombres = request.session['nombres']

    cant = 0  # cantidad de preguntas
    puntaje_pre = 0
    puntaje_nivel = 0
    punto_prerequisito = 0
    punto_nivel = 0
    HabilidadPreg = dict()
    EjePreg = dict()
    codigo_actividad = prueba[0:2]
    CantPregHabilidad = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    CantPregEje = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    PuntajesEje = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    PuntajesHabilidad = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    # indice que separa las preguntas de pre-requisito y las de nivel.
    preguntas_prueba = {'P3': 10, 'P4': 10, 'P5': 16, 'P6': 16, 'P7': 16, 'P8': 16}

    preguntas = TblPreguntas.objects.filter(siglas=codigo_actividad)

    for pregunta in preguntas:
        HabilidadPreg[pregunta.npregunta] = int(pregunta.id_habilidad.id_habilidad)
        EjePreg[pregunta.npregunta] = int(pregunta.id_eje.id_eje)
        CantPregHabilidad[int(pregunta.id_habilidad.id_habilidad)] += 1
        CantPregEje[int(pregunta.id_eje.id_eje)] += 1

    respuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=TblAlumnos.objects.get(rut_alumno=rut),
                                                    prueba_guia=pruebaGuia)

    # recorre las respuestas del alumno.
    for respuesta in respuestas:

        cant += 1

        aprobada = 0 if respuesta.aprobada < 1 else respuesta.aprobada

        if int(respuesta.npregunta) <= int(preguntas_prueba[codigo_actividad]):
            puntaje_pre += aprobada
        else:
            puntaje_nivel += aprobada

        PuntajesEje[int(EjePreg[respuesta.npregunta])] += aprobada

        PuntajesHabilidad[int(HabilidadPreg[respuesta.npregunta])] += aprobada

    # calcula los porcentaje de pre-requisito y de nivel.
    if cant > 0:
        punto_prerequisito = redondeo(puntaje_pre * 100 / int(preguntas_prueba[codigo_actividad]))
        punto_nivel = redondeo(puntaje_nivel * 100 / (cant - int(preguntas_prueba[codigo_actividad]))) if puntaje_nivel > 0 else 0

    punto_prerequisito = 1 if punto_prerequisito == 0 else punto_prerequisito
    punto_nivel = 1 if punto_nivel == 0 else punto_nivel

    h1 = redondeo(PuntajesHabilidad[1] * 100 / CantPregHabilidad[1]) if CantPregHabilidad[1] > 0 else ''
    h2 = redondeo(PuntajesHabilidad[2] * 100 / CantPregHabilidad[2]) if CantPregHabilidad[2] > 0 else ''
    h3 = redondeo(PuntajesHabilidad[3] * 100 / CantPregHabilidad[3]) if CantPregHabilidad[3] > 0 else ''
    eje1 = redondeo(PuntajesEje[1] * 100 / CantPregEje[1]) if PuntajesEje[1] > 0 else 0
    eje2 = redondeo(PuntajesEje[3] * 100 / CantPregEje[3]) if PuntajesEje[3] > 0 else 0
    eje3 = redondeo(PuntajesEje[2] * 100 / CantPregEje[2]) if PuntajesEje[2] > 0 else 0
    eje4 = redondeo(PuntajesEje[4] * 100 / CantPregEje[4]) if PuntajesEje[4] > 0 else 0
    eje5 = redondeo(PuntajesEje[5] * 100 / CantPregEje[5]) if PuntajesEje[5] > 0 else 0
    eje6 = redondeo(PuntajesEje[6] * 100 / CantPregEje[6]) if CantPregEje[6] > 0 else 0
    eje7 = redondeo(PuntajesEje[8] * 100 / CantPregEje[8]) if CantPregEje[8] > 0 else 0
    eje8 = redondeo(PuntajesEje[7] * 100 / CantPregEje[7]) if CantPregEje[7] > 0 else 0
    eje9 = redondeo(PuntajesEje[9] * 100 / CantPregEje[9]) if CantPregEje[9] > 0 else 0
    eje10 = redondeo(PuntajesEje[10] * 100 / CantPregEje[10]) if CantPregEje[10] > 0 else 0

    # obtener la fecha de inicio de la actividad.
    # actualizar la fecha de fin de la actividad.

    now = datetime.datetime.now()

    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    registro = TblAlumnoDiagnostico(rut_alumno=TblAlumnos.objects.get(rut_alumno=rut),
                                    id_actividad=TblActividades.objects.get(prueba_guia=pruebaGuia),
                                    fecha_inicio=fechaActual,
                                    fecha_fin=fechaActual,
                                    punto_prerequisito=punto_prerequisito,
                                    punto_nivel=punto_nivel,
                                    h1=h1,
                                    h2=h2,
                                    h3=h3,
                                    eje1=eje1,
                                    eje2=eje2,
                                    eje3=eje3,
                                    eje4=eje4,
                                    eje5=eje5,
                                    eje6=eje6,
                                    eje7=eje7,
                                    eje8=eje8,
                                    eje9=eje9,
                                    eje10=eje10)
    try:
        registro.save()
    except:
        print('no se guardo')

    # actualiza el campo nuevo en tabla alumno.
    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut)
    objAlumno.update(nuevo=0)

    Actividad = TblActividades.objects.filter(prueba_guia=pruebaGuia)
    descripcion = Actividad[0].descripcion_actividades

    data = {
        'prueba': prueba,
        'descripcion': descripcion,
        'nombres': nombres,
        'punto_prerequisito': punto_prerequisito,
        'punto_nivel': punto_nivel,
    }

    return render(request, 'ggalbas/resultadoDiagnostico.html', data)


def obtenerIp(request):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return HttpResponse(ip)


def unidadesAlumno(request):
    rutAlumno = request.session['rut']
    objAlumno = TblAlumnos.objects.get(rut_alumno=rutAlumno)
    objUnidades = TblUnidades.objects.get(id_unidad=25)

    listaContenidos = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno.codigo_lista,
                                                        id_unidad=objUnidades).order_by('orden')
    listaUnidades = dict()

    for result in listaContenidos:
        listaUnidades[result.id_unidad.id_unidad] = result.id_unidad.nombre_unidad

    data = {
        'nombres': request.session['nombres'],
        'nivel': request.session['nivel'],
        'rbd': request.session['rbd'],
        'listaUnidades': listaUnidades,
        'listaContenidos': listaContenidos,
    }

    return render(request, 'ggalbas/unidadesAlumno.html', data)


def contenidosAlumno(request):
    data = {
        'nombres': request.session['nombres'],
        'nivel': request.session['nivel'],
        'rbd': request.session['rbd'],
    }

    return render(request, 'ggalbas/contenidosAlumno.html', data)

def redondeo(x):
    return int(x + math.copysign(0.5, x))