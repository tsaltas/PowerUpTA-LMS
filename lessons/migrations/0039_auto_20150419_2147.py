# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0038_auto_20150419_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(blank=True, max_length=15, null=True, choices=[(b'Offline', b'Offline'), (b'Online', b'Online'), (b'Discussion', b'Discussion'), (b'Extension', b'Extension')]),
            preserve_default=True,
        ),
    ]
