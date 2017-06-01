# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20170531_1952'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user',
            new_name='UserInfo',
        ),
    ]
