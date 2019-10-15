# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblActividades(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre_actividad = models.CharField(max_length=50, blank=True, null=True)
    descripcion_actividades = models.CharField(max_length=50)
    id_tipo_actividad = models.ForeignKey('TblTipoActividad', models.DO_NOTHING, db_column='id_tipo_actividad')
    id_padre = models.IntegerField(blank=True, null=True)
    npreguntas = models.IntegerField(blank=True, null=True)
    prueba_guia = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_actividades'


class TblActividadesPreguntas(models.Model):
    id_actividad_pregunta = models.AutoField(primary_key=True)
    id_actividad = models.ForeignKey(TblActividades, models.DO_NOTHING, db_column='id_actividad')
    id_pregunta = models.ForeignKey('TblPreguntas', models.DO_NOTHING, db_column='id_pregunta')

    class Meta:
        managed = False
        db_table = 'tbl_actividades_preguntas'


class TblAdministradores(models.Model):
    rut_admin = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    apellido = models.CharField(max_length=20, blank=True, null=True)
    clave = models.CharField(max_length=30, blank=True, null=True)
    rbd = models.ForeignKey('TblInstituciones', models.DO_NOTHING, db_column='rbd', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_administradores'


class TblAlumnoActividades(models.Model):
    id_alumno_actividad = models.IntegerField(primary_key=True)
    rut_alumno = models.ForeignKey('TblAlumnos', models.DO_NOTHING, db_column='rut_alumno', blank=True, null=True)
    id_contenido_fase_actividad = models.ForeignKey('TblContenidosFasesActividades', models.DO_NOTHING, db_column='id_contenido_fase_actividad', blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    puntaje = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_alumno_actividades'


class TblAlumnoDiagnostico(models.Model):
    id_alumno_diagnostico = models.AutoField(primary_key=True)
    rut_alumno = models.ForeignKey('TblAlumnos', models.DO_NOTHING, db_column='rut_alumno', blank=True, null=True)
    id_contenido_fase_actividad = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    punto_prerequisito = models.IntegerField(blank=True, null=True)
    punto_nivel = models.IntegerField(blank=True, null=True)
    h1 = models.IntegerField(blank=True, null=True)
    h2 = models.IntegerField(blank=True, null=True)
    h3 = models.IntegerField(blank=True, null=True)
    h4 = models.IntegerField(blank=True, null=True)
    h5 = models.IntegerField(blank=True, null=True)
    eje1 = models.IntegerField(blank=True, null=True)
    eje2 = models.IntegerField(blank=True, null=True)
    eje3 = models.IntegerField(blank=True, null=True)
    eje4 = models.IntegerField(blank=True, null=True)
    eje5 = models.IntegerField(blank=True, null=True)
    eje6 = models.IntegerField(blank=True, null=True)
    eje7 = models.IntegerField(blank=True, null=True)
    eje8 = models.IntegerField(blank=True, null=True)
    eje9 = models.IntegerField(blank=True, null=True)
    eje10 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_alumno_diagnostico'


class TblAlumnoRespuestas(models.Model):
    id_alumno_respuestas = models.IntegerField(primary_key=True)
    rut_alumno = models.ForeignKey('TblAlumnos', models.DO_NOTHING, db_column='rut_alumno', blank=True, null=True)
    id_pregunta = models.ForeignKey('TblPreguntas', models.DO_NOTHING, db_column='id_pregunta', blank=True, null=True)
    respuesta = models.CharField(max_length=50, blank=True, null=True)
    puntaje = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_alumno_respuestas'


class TblAlumnos(models.Model):
    rut_alumno = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    id_pregunta = models.ForeignKey('TblPreguntausuarios', models.DO_NOTHING, db_column='id_pregunta', blank=True, null=True)
    respuesta = models.CharField(max_length=50, blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    nuevo = models.IntegerField(blank=True, null=True)
    autonomo = models.IntegerField(blank=True, null=True)
    id_producto = models.ForeignKey('TblSubproducto', models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    codigo_lista = models.ForeignKey('TblListas', models.DO_NOTHING, db_column='codigo_lista', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_alumnos'


class TblContenidoUnidad(models.Model):
    id_contenido_unidad = models.AutoField(primary_key=True)
    id_contenido = models.ForeignKey('TblContenidos', models.DO_NOTHING, db_column='id_contenido')
    id_unidad = models.ForeignKey('TblUnidades', models.DO_NOTHING, db_column='id_unidad', blank=True, null=True)
    codigo_lista = models.ForeignKey('TblListas', models.DO_NOTHING, db_column='codigo_lista')
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    orden = models.IntegerField()
    activo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_contenido_unidad'


class TblContenidos(models.Model):
    id_contenido = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    id_eje = models.ForeignKey('TblEje', models.DO_NOTHING, db_column='id_eje')
    orden = models.IntegerField()
    id_unidad = models.ForeignKey('TblUnidades', models.DO_NOTHING, db_column='id_unidad', blank=True, null=True)
    codigo = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_contenidos'


class TblContenidosFasesActividades(models.Model):
    id_contenido_fase_actividad = models.AutoField(primary_key=True)
    id_contenido = models.ForeignKey(TblContenidos, models.DO_NOTHING, db_column='id_contenido', blank=True, null=True)
    id_fase = models.ForeignKey('TblFases', models.DO_NOTHING, db_column='id_fase')
    id_actividades = models.ForeignKey(TblActividades, models.DO_NOTHING, db_column='id_actividades')
    orden = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_contenidos_fases_actividades'


class TblContenidosObjetivos(models.Model):
    id_contenidos_objetivos = models.AutoField(primary_key=True)
    id_contenido = models.ForeignKey(TblContenidos, models.DO_NOTHING, db_column='id_contenido', blank=True, null=True)
    id_objetivos_aprendizaje = models.ForeignKey('TblObjetivosAprendizaje', models.DO_NOTHING, db_column='id_objetivos_aprendizaje')

    class Meta:
        managed = False
        db_table = 'tbl_contenidos_objetivos'


class TblEje(models.Model):
    id_eje = models.AutoField(primary_key=True)
    eje = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_eje'


class TblFases(models.Model):
    id_fase = models.AutoField(primary_key=True)
    nombre_fase = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_fases'


class TblHabilidades(models.Model):
    id_habilidad = models.AutoField(primary_key=True)
    habilidad = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_habilidades'


class TblInstituciones(models.Model):
    rbd = models.IntegerField(primary_key=True)
    nombre_institucion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_instituciones'

    def __str__(self):
        return '{}'.format(self.rbd)

class TblListas(models.Model):
    codigo_lista = models.CharField(primary_key=True, max_length=30)
    rbd = models.ForeignKey(TblInstituciones, models.DO_NOTHING, db_column='rbd')
    id_nivel = models.ForeignKey('TblNiveles', models.DO_NOTHING, db_column='id_nivel')
    letra = models.CharField(max_length=3)
    rut_tutor = models.ForeignKey('TblTutores', models.DO_NOTHING, db_column='rut_tutor')
    total_alumnos = models.IntegerField()
    alumnos_registrados = models.IntegerField()
    fecha_ingreso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_listas'

    def __str__(self):
        return '{}'.format(self.codigo_lista)


class TblNiveles(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nivel = models.CharField(max_length=20)
    categoria = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'tbl_niveles'

    def __str__(self):
        return '{}'.format(self.id_nivel)


class TblObjetivosAprendizaje(models.Model):
    id_objetivos_aprendizaje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_objetivos_aprendizaje'


class TblPlan(models.Model):
    id_plan = models.IntegerField(primary_key=True)
    rut_alumno = models.ForeignKey(TblAlumnos, models.DO_NOTHING, db_column='rut_alumno')
    id_contenido_unidad = models.ForeignKey(TblContenidoUnidad, models.DO_NOTHING, db_column='id_contenido_unidad', blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_plan'


class TblPlanAutonomo(models.Model):
    id_plan_autonomo = models.AutoField(primary_key=True)
    rut_alumno = models.ForeignKey(TblAlumnos, models.DO_NOTHING, db_column='rut_alumno')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_plan_autonomo'


class TblPreguntas(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    pregunta = models.TextField()
    respuesta = models.TextField()
    id_eje = models.ForeignKey(TblEje, models.DO_NOTHING, db_column='id_eje', blank=True, null=True)
    id_habilidad = models.ForeignKey(TblHabilidades, models.DO_NOTHING, db_column='id_habilidad', blank=True, null=True)
    id_tipo_pregunta = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_preguntas'


class TblPreguntausuarios(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    pregunta = models.CharField(max_length=30)
    nombreusuarioregistro = models.CharField(max_length=30)
    fecharegistro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_preguntausuarios'

    def __str__(self):
        return '{}'.format(self.id_pregunta)


class TblRegistroipAlumno(models.Model):
    rut_alumno = models.ForeignKey(TblAlumnos, models.DO_NOTHING, db_column='rut_alumno')
    ip = models.CharField(max_length=30)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_registroip_alumno'


class TblSubproducto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=20)
    url = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'tbl_subproducto'

    def __str__(self):
        return '{}'.format(self.id_producto)


class TblTipoActividad(models.Model):
    id_tipo_actividad = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_tipo_actividad'


class TblTipoPregunta(models.Model):
    id_tipo_pregunta = models.AutoField(primary_key=True)
    tipo_pregunta = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tbl_tipo_pregunta'


class TblTutores(models.Model):
    rut_tutor = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tbl_tutores'


class TblUnidades(models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre_unidad = models.CharField(max_length=255)
    id_nivel = models.ForeignKey(TblNiveles, models.DO_NOTHING, db_column='id_nivel', blank=True, null=True)
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_unidades'