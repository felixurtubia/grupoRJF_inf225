from django.db import models
from django.contrib.auth.models import Permission, User
from datetime import datetime


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField
    cargo = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    perfil = models.CharField(max_length=200, choices=(('operador', 'Operador'),
                                                       ('supervisor', 'Supervisor'), ('jefe', 'Jefe')))
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Guardia(models.Model):
    designado = models.ForeignKey(Empleado)
    reporte = models.CharField(max_length=500)
    inicio = models.DateField
    fin = models.DateField

    def __str__(self):
        return "Guardia de %s, desde %s hasta %s.", self.designado.user.first_name, self.inicio, self.fin



class Ticket(models.Model):
    titulo = models.CharField(max_length=300)
    asunto = models.CharField(max_length=500, null=True)
    contenido = models.CharField(max_length=500, null=True)
    prioridad = models.CharField(max_length=15, choices=(('Urgente', 'Urgente'), ('Estandar', 'Estandar'),
                                                         ('Baja', 'Baja')))
    impacto = models.CharField(max_length=8, null=True)
    direccionamiento = models.CharField(max_length=10, null=True)
    cybersystem = models.CharField(max_length=10, null=True)
    fecha_apertura = models.DateField(auto_now_add=True)
    fecha_cierre = models.DateField(null=True)
    # Estados
    cerrado = models.BooleanField(default=False)
    fecha_aplazo = models.DateField(null=True)
    asignado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

    creador = models.ForeignKey(User, related_name='creador')
    encargado = models.ForeignKey(User, related_name='encargado', null=True)
    cerrador = models.ForeignKey(User, related_name='cerrador', null =True)

    def __str__(self):
        return self.titulo


# Tipo de Ticket
class Correo(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    email_atacante = models.CharField(max_length=100)
    email_suplantado = models.CharField(max_length=100)
    asunto_correo = models.CharField(max_length=500)
    nro_afectados = models.IntegerField(default=0)
    catalogamiento = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    subtipo = models.CharField(max_length=200)
    clase = models.CharField(max_length=200)


class DetalleContenido(models.Model):
    correo = models.OneToOneField(Correo, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
    link_enmascarado = models.CharField(max_length=100)
    dominio = models.CharField(max_length=300)
    adjunto_name = models.CharField(max_length=100)


class DetalleCorreo(models.Model):
    correo = models.OneToOneField(Correo, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100)
    uurr = models.CharField(max_length=50)
    # tecnico
    fecha_recepcion = models.DateField
    comprometido = models.BooleanField(default=False)
    comentario = models.CharField(max_length=200, default='')


# Tipo de Ticket
class Evento(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    signo = models.IntegerField
    geolocalizacion = models.CharField(max_length=10)
    puerto_destino = models.IntegerField
    ip_origen = models.CharField(max_length=15)
    ip_destino = models.CharField(max_length=15)
    servicio_afectado = models.CharField(max_length=250)
    alerta_id = models.CharField(max_length=25)
    alerta_name = models.CharField(max_length=25)
    hashsha1 = models.CharField(max_length=150)
    hashsha2 = models.CharField(max_length=150)
    hashshamd5 = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50)
    subtipo = models.CharField(max_length=200)
    clase = models.CharField(max_length=200)


#Tipo de Ticket
class Trabajo(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    inicio = models.DateField
    equipo = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)


class Keyword(models.Model):
    nombre = models.CharField(max_length=100)
    ticket = models.ForeignKey(User)

    def __str__(self):
        return self.nombre


class FileData(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    visada = models.BooleanField(default=False)
    data_title = models.CharField(max_length=250)
    data_file = models.FileField(default='')

    def __str__(self):
        return self.data_title


class TextData(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    visada = models.BooleanField(default=False)
    data_title = models.CharField(max_length=250)
    data_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.data_title


class VinculoHijo(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_hijo = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='relacion_hijo')
    vinculo = models.CharField(max_length=50)


class VinculoPadre(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_padre = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='relacion_padre')
    vinculo = models.CharField(max_length=50)