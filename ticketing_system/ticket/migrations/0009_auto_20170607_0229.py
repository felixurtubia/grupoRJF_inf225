# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_auto_20170607_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='tiempo_aplazado',
            new_name='fecha_aplazo',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='aplazado',
        ),
    ]
