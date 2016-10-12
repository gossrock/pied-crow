# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Bell Name')),
                ('gpio_pin', models.IntegerField(verbose_name='GPIO Pin Number')),
            ],
        ),
        migrations.CreateModel(
            name='BellRing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Ring Time')),
                ('note', models.CharField(max_length=200, verbose_name='Note')),
            ],
        ),
        migrations.CreateModel(
            name='RingPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Ring Pattern Name')),
                ('repeat', models.BooleanField(verbose_name='Pattern Repeats')),
            ],
        ),
        migrations.CreateModel(
            name='RingPatternPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_off', models.BooleanField(verbose_name='On/Off')),
                ('duration', models.FloatField(verbose_name='Duration of Part')),
                ('ring_pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BellSchedule.RingPattern')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Schedule Name')),
            ],
        ),
        migrations.AddField(
            model_name='bellring',
            name='ring_pattern',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BellSchedule.RingPattern'),
        ),
        migrations.AddField(
            model_name='bellring',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BellSchedule.Schedule'),
        ),
    ]
