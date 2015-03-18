# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0018_auto_20150311_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(related_name='activities', to='lessons.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='logo',
            field=models.ImageField(upload_to=b'tag_logos', blank=True),
            preserve_default=True,
        ),
    ]
