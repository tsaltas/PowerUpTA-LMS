# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_auto_20150129_1717'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='curriculumactivityrelationship',
            unique_together=set([('curriculum', 'activity'), ('curriculum', 'number')]),
        ),
    ]
