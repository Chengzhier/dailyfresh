# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uaddress',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='ucode',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AlterField(
            model_name='user',
            name='uemail',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='upasswd',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='ushou',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='utel',
            field=models.CharField(default=b'', max_length=11),
        ),
    ]
