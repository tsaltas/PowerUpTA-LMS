# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0035_auto_20150419_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='step_activity',
            field=models.ForeignKey(blank=True, to='lessons.Activity', null=True),
            preserve_default=True,
        ),
    ]
