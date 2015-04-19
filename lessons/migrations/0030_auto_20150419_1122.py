# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0029_auto_20150418_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='logo',
            field=models.ImageField(default=b'tag_logos/gray-box.jpg', null=True, upload_to=b'tag_logos', blank=True),
            preserve_default=True,
        ),
    ]
