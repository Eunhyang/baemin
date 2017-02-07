# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='category',
            field=models.CharField(choices=[('kr', '한식'), ('ch', '중식'), ('jp', '일식')], default='kr', max_length=2),
        ),
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='메뉴 이미지'),
        ),
    ]