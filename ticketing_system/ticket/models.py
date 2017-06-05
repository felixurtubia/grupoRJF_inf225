from django.db import models
from django.contrib.auth.models import Permission, User


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField
    cargo = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    perfil = models.CharField(max_length=200, choices=(('administrador', 'administrador'), ('operador', 'operador'),
                                                       ('supervisor', 'supervisor'), ('jefe', 'jefe')))
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + self.user.last_name + ' - ' + self.perfil


class Ticket(models.Model):
    titulo = models.CharField(max_length=300)
    asunto = models.CharField(max_length=500)
    contenido = models.CharField(max_length=500)
    prioridad = models.CharField(max_length=15, choices=(('urgente', 'urgente'), ('estandar', 'estandar'),
                                                         ('baja', 'baja')))
    # para que supervisor cierre ticket
    cerrado = models.BooleanField(default=False)
    # para que supervisor aplaze ticket
    aplazado = models.BooleanField(default=False)
    tiempo_aplazado = models.DateField
    # para ver si se ha asignado o no
    asignado = models.BooleanField(default=False)
    # ticket completo, enviado a supervisor para revisar y cerrar
    resuelto = models.BooleanField(default=False)

    creador = models.ForeignKey(User, related_name='creador')
    encargado = models.ForeignKey(User, related_name='encargado', null=True)
    cerrador = models.ForeignKey(User, related_name='cerrador', null =True)

    def __str__(self):
        return self.titulo


class Keyword(models.Model):
    nombre = models.CharField(max_length=100)
    ticket = models.ForeignKey(User)

    def __str__(self):
        return self.nombre


class FileData(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    data_title = models.CharField(max_length=250)
    data_file = models.FileField(default='')

    def __str__(self):
        return self.data_title

class TextData(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    data_title = models.CharField(max_length=250)
    data_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.data_title
