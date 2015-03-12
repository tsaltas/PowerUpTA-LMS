# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0017_auto_20150311_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='resources',
            field=models.ManyToManyField(related_name='activities', to='lessons.Resource', blank=True),
            preserve_default=True,
        ),
    ]
