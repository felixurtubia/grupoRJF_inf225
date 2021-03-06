# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-26 12:09
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0020_auto_20170825_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='perfil',
            field=models.CharField(choices=[('operador', 'Operador'), ('supervisor', 'Supervisor'), ('jefe', 'Jefe'), ('administrador', 'Administrador')], max_length=200),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Ticket'),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='usuario_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fecha_aplazo',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
