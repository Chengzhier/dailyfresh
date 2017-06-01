# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upaswd', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upasswd', models.CharField(max_length=20)),
                ('ushou', models.CharField(max_length=20)),
                ('uemail', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=50)),
                ('utel', models.CharField(max_length=11)),
                ('ucode', models.CharField(max_length=6)),
            ],
        ),
    ]
