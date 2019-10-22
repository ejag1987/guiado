import json
import random
import string
import datetime
import base64
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect

from ggalbas.models import TblAlumnos, TblListas, TblPreguntausuarios, TblSubproducto, TblRegistroipAlumno, TblNiveles, TblInstituciones, TblActividades, TblTipoActividad, TblAlumnoActividades, TblAlumnoRespuestas
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
            ## Se debe consultar en tbl_actividades para saber en que actividad se encuentra
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
    actividad = TblActividades.objects.filter(prueba_guia=pruebaGuia)
    rutAlumno= request.session['rut']

    if actividad:
        descripcion= actividad[0].descripcion_actividades
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
            descripcion= 'sin'
        else:
            descripcion= 'no hay actividad'

    preguntas = Preguntas2Basico.objects.using('e_test').filter(idprueba=pruebaGuia)
    respuestas= TblAlumnoRespuestas.objects.filter(rut_alumno=rutAlumno, prueba_guia=pruebaGuia)

    if respuestas:
        npregunta=  int(respuestas[-1].npregunta)+1
        img = base64.b64encode(preguntas[npregunta].imagen).decode()
        posiciones = str(preguntas[npregunta].posiciones_botones)
        pos_boton = posiciones.replace('!', "")
        lista_pos = pos_boton.split(',')
        posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
        npreg = preguntas[npregunta].npregunta
        tipoEjercicio = preguntas[npregunta].tipo_ejercicio
    else:
        img= base64.b64encode(preguntas[0].imagen).decode()
        posiciones = str(preguntas[0].posiciones_botones)
        pos_boton= posiciones.replace('!',"")
        lista_pos= pos_boton.split(',')
        posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
        npreg= preguntas[0].npregunta
        tipoEjercicio = preguntas[0].tipo_ejercicio

    data = {
        'title': 'imagen-ejercicio',
        'img': img,
        'prueba': prueba,
        'descripcion': descripcion,
        'botones': posicion_boton,
        'nejercicio': npreg,
        'tipoE': tipoEjercicio,
    }

    ##return HttpResponse(cantidades)
    return render(request, 'ggalbas/visorActividades.html', data)

def guardaRespuesta(request):
    respuesta1 = request.POST['fill1']


    responde = json.dumps(respuesta1)

    return HttpResponse (respuesta1)

def resultadoDiagnostico(request):
    
    nombres = request.session['nombres']    
    
    '''id_contenido_fase_actividad=1

    punto_prerequisito,punto_nivel,h1,h2,h3,eje1,eje2,eje3,eje4,eje5,eje6,eje7,eje8,eje9,eje10 = calculoDiagnostico(request)

    #obtener la fecha deinicio de la actividad.
    fecha_inicio

    #actualizar la fecha de fin de la actividad.


    #guarda el resultado en tabla TblAlumnoDiagnostico
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    
    registroAlumnoDiagnostico = TblAlumnoDiagnostico(rut_alumno=obj_alumno,
                                                     id_contenido_fase_actividad=id_contenido_fase_actividad,
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
    registroAlumnoDiagnostico.save() '''
   
    return render(request, 'ggalbas/resultadoDiagnostico.html',{'punto_prerequisito':30, 'punto_nivel':30, 'nombres': nombres })

def calculoDiagnostico(request):

    pruebaGuia = 11
    #pruebaGuia = request.session['prueba_guia']
    prueba = request.session['prueba']    
    rut        = request.session['rut']
    
    # obtengo solo los dos primeros caracteres para determinar cual actividad es.
    codigo_actividad = prueba[0:2]

    #consulta el objeto alumno
    obj_alumno = TblAlumnos.objects.get(rut_alumno=rut)

    #consulta los resultados del alumno
    TblAlumnoRespuestas_set =TblAlumnoRespuestas.objects.filter(rut_alumno=obj_alumno,prueba_guia=pruebaGuia)

    #consulta los ejes y habilidades de las preguntas de la actividad.
    TblPreguntas_set = TblPreguntas.objects.filter(siglas=codigo_actividad)

    # indice que separa las preguntas de pre-requisito y las de nivel.
    preguntas_prueba = {'P3': 10, 'P4': 10,'P5': 16, 'P6': 16, 'P7': 16, 'P8': 16}
   
    # cantidad de preguntas
    cant = 0

    # cantidad de respuestas correctas en pre-requisito y nivel.
    puntaje_pre = 0
    puntaje_nivel = 0

    punto_prerequisito = 0
    punto_nivel = 0
         
    # Contar la cantidad de preguntas para cada habilidad y eje.
    HabilidadPreg= dict()

    EjePreg = dict()

    CantPregHabilidad = dict()

    CantPregEje = dict()

    for result in TblPreguntas_set:
                
        HabilidadPreg[result.npregunta] = int(result.id_habilidad)

        EjePreg[result.npregunta] = int(result.id_eje)

        if CantPregHabilidad[int(result.id_habilidad)] =='':
            CantPregHabilidad[int(result.id_habilidad)] = 0
    
        CantPregHabilidad[int(result.id_habilidad)] += 1 

        if CantPregEje[int(result.id_eje)] =='':
            CantPregEje[int(result.id_eje)] = 0
    
        CantPregEje[int(result.id_eje)] += 1 


    # recorre las respuestas del alumno.
    PuntajesEje = dict()
    PuntajesHabilidad = dict()

    for record in TblAlumnoRespuestas_set:

        cant += 1

        aprobada = 0 if record.aprobada < 1 else record.aprobada
      
        if int(record.npregunta) <= int(preguntas_prueba[codigo_actividad]):
            puntaje_pre += aprobada
        else:
            puntaje_nivel += aprobada
        
        if PuntajesEje[int(EjePreg[record.npregunta])] == '':
            PuntajesEje[int(EjePreg[record.npregunta])]= 0

        PuntajesEje[int(EjePreg[record.npregunta])] += aprobada

        if PuntajesHabilidad[int(HabilidadPreg[record.npregunta])] == '':
            PuntajesHabilidad[int(HabilidadPreg[record.npregunta])]=0

        PuntajesHabilidad[int(HabilidadPreg[record.npregunta])] += aprobada

        
    # calcula los porcentaje de pre-requisito y de nivel.   
    if cant > 0:
        punto_prerequisito = round((puntaje_pre*100)/int(preguntas_prueba[codigo_actividad]))
        punto_nivel = round((puntaje_nivel*100)/(cant-int(preguntas_prueba[codigo_actividad]))) if puntaje_nivel > 0 else 0

    punto_prerequisito = 1 if punto_prerequisito == 0 else punto_prerequisito
    punto_nivel  =  1 if punto_nivel == 0 else punto_nivel        
    h1    = (PuntajesHabilidad[1]*100)/(CantPregHabilidad[1]) if CantPregHabilidad[1] > 0 else ''
    h2    = (PuntajesHabilidad[2]*100)/(CantPregHabilidad[2]) if CantPregHabilidad[2] > 0 else ''
    h3    = (PuntajesHabilidad[3]*100)/(CantPregHabilidad[3]) if CantPregHabilidad[3] > 0 else ''
    eje1  = (PuntajesEje[1]*100)/(CantPregEje[1]) if PuntajesEje[1] > 0 else 0
    eje2  = (PuntajesEje[3]*100)/(CantPregEje[3]) if PuntajesEje[3] > 0 else 0
    eje3  = (PuntajesEje[2]*100)/(CantPregEje[2]) if PuntajesEje[2] > 0 else 0
    eje4  = (PuntajesEje[4]*100)/(CantPregEje[4]) if PuntajesEje[4] > 0 else 0
    eje5  = (PuntajesEje[5]*100)/(CantPregEje[5]) if PuntajesEje[5] > 0 else 0
    eje6  = (PuntajesEje[6]*100)/(CantPregEje[6]) if CantPregEje[6] > 0 else 0
    eje7  = (PuntajesEje[8]*100)/(CantPregEje[8]) if CantPregEje[8] > 0 else 0
    eje8  = (PuntajesEje[7]*100)/(CantPregEje[7]) if CantPregEje[7] > 0 else 0
    eje9  = (PuntajesEje[9]*100)/(CantPregEje[9]) if CantPregEje[9] > 0 else 0
    eje10 = (PuntajesEje[10]*100)/(CantPregEje[10]) if CantPregEje[10] > 0 else 0
    
    return punto_prerequisito,punto_nivel,h1, h2,h3, eje1, eje2, eje3, eje4, eje5, eje6, eje7, eje8, eje9, eje10
