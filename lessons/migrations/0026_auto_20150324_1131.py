# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0025_auto_20150323_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrelationship',
            name='rel_type',
            field=models.CharField(max_length=3, verbose_name=b'Relationship Type', choices=[(b'SUB', b'sub-activity'), (b'SUP', b'super-activity'), (b'EXT', b'extension')]),
            preserve_default=True,
        ),
    ]
