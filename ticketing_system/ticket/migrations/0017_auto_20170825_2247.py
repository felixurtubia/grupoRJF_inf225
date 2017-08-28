# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-26 01:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0016_auto_20170825_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 26, 1, 47, 25, 641783, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fecha_aplazo',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 26, 1, 47, 25, 632255, tzinfo=utc), null=True),
        ),
    ]
