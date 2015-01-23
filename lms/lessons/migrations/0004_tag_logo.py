# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20150121_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='logo',
            field=models.ImageField(default=b'/media/tag_logos/default.jpg', upload_to=b'tag_logos'),
            preserve_default=True,
        ),
    ]
