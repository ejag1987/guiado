# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class Asignatura(models.Model):
    asig_id = models.AutoField(primary_key=True)
    asig_nombre = models.CharField(unique=True, max_length=45)
    asig_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignatura'


class Auditoria(models.Model):
    datetime = models.DateTimeField()
    programa = models.CharField(max_length=80, blank=True, null=True)
    usuario = models.CharField(max_length=80, blank=True, null=True)
    accion = models.CharField(max_length=80, blank=True, null=True)
    tabla = models.CharField(max_length=80, blank=True, null=True)
    campo = models.CharField(max_length=80, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'


class Configuracion(models.Model):
    clave = models.CharField(primary_key=True, max_length=100)
    valor = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'configuracion'


class Encuestas(models.Model):
    codprueba = models.CharField(primary_key=True, max_length=20)
    fecha_apertura = models.DateField()
    toma = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'encuestas'


class Objetivos(models.Model):
    objcodigo = models.AutoField(primary_key=True)
    objnombre = models.CharField(unique=True, max_length=100)
    objdescripcion = models.CharField(max_length=255)
    objtiene_subvalor = models.IntegerField()
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivos'


class Objetivossubvalores(models.Model):
    idobjetivosubvalor = models.AutoField(primary_key=True)
    objcodigo = models.IntegerField()
    idobjetivovalor = models.IntegerField()
    objsubvalor = models.CharField(max_length=255)
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivossubvalores'
        unique_together = (('objcodigo', 'idobjetivovalor', 'objsubvalor'),)


class Objetivosvalores(models.Model):
    idobjetivovalor = models.AutoField(primary_key=True)
    objcodigo = models.IntegerField()
    objvalor = models.CharField(max_length=255)
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivosvalores'
        unique_together = (('objcodigo', 'objvalor'),)


class Portadas(models.Model):
    tipoactividad = models.CharField(primary_key=True, max_length=20)
    nivel = models.IntegerField()
    etapa = models.IntegerField()
    portada = models.TextField(blank=True, null=True)
    portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    portada_ancho = models.PositiveIntegerField(blank=True, null=True)
    portada_alto = models.PositiveIntegerField(blank=True, null=True)
    portada_tamano = models.PositiveIntegerField(blank=True, null=True)
    s_portada = models.TextField()
    s_portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_portada_ancho = models.IntegerField(blank=True, null=True)
    s_portada_alto = models.IntegerField(blank=True, null=True)
    s_portada_tamano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portadas'
        unique_together = (('tipoactividad', 'nivel', 'etapa'),)


class Preguntas(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    descpregunta = models.TextField()
    alternativa1 = models.TextField()
    alternativa2 = models.TextField()
    alternativa3 = models.TextField()
    alternativa4 = models.TextField()
    alternativa5 = models.TextField()
    imagen = models.TextField(blank=True, null=True)
    idprueba = models.IntegerField()
    tipo_ejercicio = models.IntegerField()
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntas'
        unique_together = (('npregunta', 'idprueba'),)


class Preguntas2Basico(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idprueba = models.IntegerField()
    descpregunta = models.TextField(blank=True, null=True)
    alternativa1 = models.TextField(blank=True, null=True)
    alternativa2 = models.TextField(blank=True, null=True)
    alternativa3 = models.TextField(blank=True, null=True)
    alternativa4 = models.TextField(blank=True, null=True)
    alternativa5 = models.TextField(blank=True, null=True)
    alternativa6 = models.TextField(blank=True, null=True)
    alternativa7 = models.TextField(blank=True, null=True)
    alternativa8 = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    solucion_texto = models.TextField(blank=True, null=True)
    solucion_imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField()
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    solucion_imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    posiciones_botones = models.CharField(max_length=250, blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    s_imagen = models.TextField(blank=True, null=True)
    s_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    s_imagen_alto = models.IntegerField(blank=True, null=True)
    s_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_imagen_tamano = models.IntegerField(blank=True, null=True)
    s_solucion_imagen = models.TextField(blank=True, null=True)
    s_solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    s_solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    alternativa9 = models.TextField(blank=True, null=True)
    alternativa10 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntas2basico'
        unique_together = (('npregunta', 'idprueba'),)


class PreguntasInstancias(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    ninstancias = models.IntegerField()
    instancia1 = models.TextField(blank=True, null=True)
    instancia2 = models.TextField(blank=True, null=True)
    instancia3 = models.TextField(blank=True, null=True)
    instancia4 = models.TextField(blank=True, null=True)
    instancia5 = models.TextField(blank=True, null=True)
    nitemsintancias = models.IntegerField()
    instancia6 = models.TextField(blank=True, null=True)
    instancia7 = models.TextField(blank=True, null=True)
    instancia8 = models.TextField(blank=True, null=True)
    instancia9 = models.TextField(blank=True, null=True)
    instancia10 = models.TextField(blank=True, null=True)
    instancia11 = models.TextField(blank=True, null=True)
    instancia12 = models.TextField(blank=True, null=True)
    respuesta_pregunta = models.TextField()
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'preguntas_instancias'
        unique_together = (('idprueba', 'npregunta'),)


class PreguntasRecomendacion(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    recomendacion = models.TextField()

    class Meta:
        managed = False
        db_table = 'preguntas_recomendacion'
        unique_together = (('idprueba', 'npregunta'),)


class Preguntasobjetivos(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    objcodigo = models.IntegerField()
    idobjetivovalor = models.IntegerField()
    idobjetivosubvalor = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'preguntasobjetivos'
        unique_together = (('idprueba', 'npregunta', 'objcodigo', 'idobjetivovalor', 'idobjetivosubvalor'),)


class Pruebas(models.Model):
    codprueba = models.CharField(unique=True, max_length=20, blank=True, null=True)
    descprueba = models.CharField(max_length=45)
    npreguntas = models.IntegerField()
    idprueba = models.AutoField(primary_key=True)
    detallecontenido = models.TextField()
    tipo = models.IntegerField()
    asig_id = models.IntegerField()
    serie_id = models.IntegerField()
    vigente = models.IntegerField()
    estado = models.IntegerField()
    fecha_ultima_modificacion = models.DateTimeField()
    tipom = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pruebas'

    def __str__(self):
        return '{}'.format(self.codprueba)


class PruebasEjercicios(models.Model):
    n_pregunta = models.PositiveIntegerField()
    descripcion = models.TextField()
    eje = models.PositiveIntegerField()
    habilidad = models.PositiveIntegerField()
    cod_prueba = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'pruebas_ejercicios'
        unique_together = (('cod_prueba', 'n_pregunta'),)


class PruebasTipo(models.Model):
    idtipo = models.IntegerField(primary_key=True)
    descripciontipo = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'pruebas_tipo'


class Pruebasmaterial(models.Model):
    idmaterial = models.AutoField(primary_key=True)
    idprueba = models.IntegerField()
    material = models.TextField(blank=True, null=True)
    material_tipo = models.CharField(max_length=255, blank=True, null=True)
    material_tamano = models.IntegerField(blank=True, null=True)
    material_nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pruebasmaterial'


class Pruebasniveles(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    curso = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pruebasniveles'
        unique_together = (('idprueba', 'curso'),)


class Pruebasobjetivos(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    objcodigo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pruebasobjetivos'
        unique_together = (('idprueba', 'objcodigo'),)


class Seguridad(models.Model):
    usuario = models.CharField(primary_key=True, max_length=15)
    clave = models.CharField(max_length=15)
    userlevel = models.IntegerField(db_column='UserLevel')  # Field name made lowercase.
    nombre = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'seguridad'


class Serie(models.Model):
    serie_id = models.AutoField(primary_key=True)
    serie_nombre = models.CharField(unique=True, max_length=45)
    serie_descripcion = models.TextField(blank=True, null=True)
    vigente = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'serie'


class Userlevelpermissions(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    tablename = models.CharField(max_length=80)
    permission = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userlevelpermissions'
        unique_together = (('userlevelid', 'tablename'),)


class Userlevels(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    userlevelname = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'userlevels'
