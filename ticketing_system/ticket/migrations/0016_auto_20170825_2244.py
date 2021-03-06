# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-26 01:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0015_auto_20170825_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 25, 22, 44, 18, 360130)),
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='tipo',
            field=models.CharField(choices=[('TAsignado', 'Ticket asignado'), ('TCerrado', 'Ticket cerrado'), ('TAplazado', 'Ticket aplazado'), ('TCreado', 'Ticket Creado'), ('TEliminado', 'Ticket Eliminado'), ('TEditado', 'Ticket Editado'), ('DCreada', 'Data nueva'), ('DA', 'Data aprobada'), ('DR', 'Data Rechazada')], max_length=200),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fecha_aplazo',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 25, 22, 44, 18, 352278), null=True),
        ),
    ]
