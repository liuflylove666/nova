# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-18 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nova', '0061_auto_20171215_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('is_mail', models.CharField(blank=True, max_length=80, null=True, verbose_name='\u662f\u5426\u53d1\u9001')),
                ('content', models.CharField(blank=True, max_length=2000, null=True, verbose_name='\u5185\u5bb9')),
                ('mail_time', models.BigIntegerField(blank=True, null=True, verbose_name='\u53d1\u9001\u65f6\u95f4')),
            ],
        ),
    ]
