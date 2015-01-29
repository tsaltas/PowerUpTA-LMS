# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20150129_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='video',
            new_name='video_url',
        ),
    ]
