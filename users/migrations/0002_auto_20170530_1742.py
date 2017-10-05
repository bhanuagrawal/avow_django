# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_following', to='users.Users')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
            options={
                'ordering': ('user',),
                'db_table': 'follow',
            },
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('user', 'following')]),
        ),
    ]
