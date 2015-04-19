# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0034_auto_20150419_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='activity',
            field=models.ForeignKey(related_name='steps', to='lessons.Activity'),
            preserve_default=True,
        ),
    ]
