# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_remove_curriculum_activities'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityrelationship',
            options={'verbose_name': 'activity relationship', 'verbose_name_plural': 'activity relationships'},
        ),
        migrations.AlterModelOptions(
            name='curriculumactivityrelationship',
            options={'verbose_name': 'curriculum relationship', 'verbose_name_plural': 'curriculum relationships'},
        ),
        migrations.AlterUniqueTogether(
            name='curriculumactivityrelationship',
            unique_together=set([('curriculum', 'activity', 'number')]),
        ),
    ]
