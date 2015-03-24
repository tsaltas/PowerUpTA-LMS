# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0023_auto_20150323_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'Language', b'Language'), (b'Technology', b'Technology'), (b'Difficulty', b'Difficulty'), (b'Length', b'Length'), (b'Concept', b'Concept')]),
            preserve_default=True,
        ),
    ]
