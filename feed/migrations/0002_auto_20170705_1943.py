# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170705_1943'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ('post',),
                'db_table': 'post_receiver',
            },
        ),
        migrations.AlterField(
            model_name='userpost',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='postreceiver',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.UserPost'),
        ),
        migrations.AddField(
            model_name='postreceiver',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users'),
        ),
    ]
