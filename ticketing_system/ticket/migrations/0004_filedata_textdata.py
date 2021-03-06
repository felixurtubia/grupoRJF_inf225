# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20170605_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_title', models.CharField(max_length=250)),
                ('data_file', models.FileField(default='', upload_to='')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Ticket')),
            ],
        ),
        migrations.CreateModel(
            name='TextData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_title', models.CharField(max_length=250)),
                ('data_text', models.CharField(max_length=1000)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.Ticket')),
            ],
        ),
    ]
