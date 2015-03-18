# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0019_auto_20150317_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='logo',
            field=models.ImageField(upload_to=b'tag_logos'),
            preserve_default=True,
        ),
    ]
