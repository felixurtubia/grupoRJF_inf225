# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0010_auto_20170615_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vinculohijo',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='vinculohijo',
            name='ticket_hijo',
        ),
        migrations.RemoveField(
            model_name='vinculopadre',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='vinculopadre',
            name='ticket_padre',
        ),
        migrations.DeleteModel(
            name='VinculoHijo',
        ),
        migrations.DeleteModel(
            name='VinculoPadre',
        ),
    ]