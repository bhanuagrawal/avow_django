# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-15 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170705_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='status',
            field=models.CharField(default='active', max_length=50),
            preserve_default=False,
        ),
    ]
