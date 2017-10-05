# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170530_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='AndroidDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(to='users.Users')),
            ],
            options={
                'ordering': ('user',),
                'db_table': 'android_devices',
            },
        ),
    ]
