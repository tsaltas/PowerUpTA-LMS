# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_auto_20150129_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculumactivityrelationship',
            options={'ordering': ['curriculum', 'number'], 'verbose_name': 'curriculum relationship', 'verbose_name_plural': 'curriculum relationships'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(blank=True, max_length=3, choices=[(b'OFF', b'Offline'), (b'ONL', b'Online'), (b'DIS', b'Discussion'), (b'EXT', b'Extension')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activityrelationship',
            name='from_activity',
            field=models.ForeignKey(related_name='relationships_from', to='lessons.Activity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activityrelationship',
            name='to_activity',
            field=models.ForeignKey(related_name='relationships_to', to='lessons.Activity'),
            preserve_default=True,
        ),
    ]
