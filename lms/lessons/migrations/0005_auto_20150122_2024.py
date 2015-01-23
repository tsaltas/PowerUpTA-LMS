# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_tag_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='lessons',
            field=models.ManyToManyField(related_name='curricula', to='lessons.Lesson'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='logo',
            field=models.ImageField(default=b'tag_logos/default.jpg', upload_to=b'tag_logos'),
            preserve_default=True,
        ),
    ]
