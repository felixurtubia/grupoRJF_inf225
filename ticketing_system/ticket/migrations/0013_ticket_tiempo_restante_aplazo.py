# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0012_auto_20170616_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='tiempo_restante_aplazo',
            field=models.DurationField(null=True),
        ),
    ]