# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='aplazado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='asignado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='cerrado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='resuelto',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='cerrador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cerrador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='encargado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encargado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='prioridad',
            field=models.CharField(choices=[('urgente', 'urgente'), ('estandar', 'estandar'), ('baja', 'baja')], max_length=15),
        ),
    ]