# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0039_auto_20150419_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='logo',
            field=models.ImageField(default=b'gray-box.jpg', null=True, upload_to=b'tag_logos', blank=True),
            preserve_default=True,
        ),
    ]
