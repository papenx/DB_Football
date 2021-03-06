# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Football', '0005_auto_20170501_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='do',
            name='Match_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Football.Match', verbose_name='Игра'),
        ),
        migrations.RemoveField(
            model_name='do',
            name='Player_key',
        ),
        migrations.AddField(
            model_name='do',
            name='Player_key',
            field=models.ManyToManyField(null=True, to='Football.Player', verbose_name='Игроки'),
        ),
        migrations.AlterField(
            model_name='player',
            name='Name',
            field=models.CharField(max_length=256, verbose_name='ФИО игрока'),
        ),
    ]
