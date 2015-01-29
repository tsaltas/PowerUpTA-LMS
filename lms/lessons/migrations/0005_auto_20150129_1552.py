# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_auto_20150129_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrelationship',
            name='rel_type',
            field=models.CharField(max_length=3, verbose_name=b'Relationship Type', choices=[(b'SUB', b'Sub-activity'), (b'SUP', b'Super-activity'), (b'EXT', b'Extension')]),
            preserve_default=True,
        ),
    ]
