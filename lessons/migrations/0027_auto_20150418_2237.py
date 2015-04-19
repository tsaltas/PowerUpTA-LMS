# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0026_auto_20150324_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.CharField(max_length=15, choices=[(b'Language', b'Language'), (b'Technology', b'Technology'), (b'Difficulty', b'Difficulty'), (b'Length', b'Length'), (b'Concept', b'Concept'), (b'Misc', b'Miscellaneous')]),
            preserve_default=True,
        ),
    ]
