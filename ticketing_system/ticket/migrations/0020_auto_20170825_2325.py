# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-26 02:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0019_auto_20170825_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='usuario_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
