# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_auto_20150129_1712'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='curriculumactivityrelationship',
            unique_together=set([('curriculum', 'number')]),
        ),
    ]
