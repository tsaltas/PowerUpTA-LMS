# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_auto_20150129_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurriculumActivityRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('activity', models.ForeignKey(related_name='curriculum_relationships', to='lessons.Activity')),
                ('curriculum', models.ForeignKey(related_name='activity_relationships', to='lessons.Curriculum')),
            ],
            options={
                'verbose_name': 'relationship',
                'verbose_name_plural': 'relationships',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='curriculumactivityrelationship',
            unique_together=set([('curriculum', 'activity')]),
        ),
        migrations.AlterField(
            model_name='activityrelationship',
            name='rel_type',
            field=models.CharField(max_length=3, verbose_name=b'Relationship Type', choices=[(b'SUB', b'sub-activity'), (b'SUP', b'super-activity'), (b'EXT', b'extension')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='length_hours',
            field=models.IntegerField(verbose_name=b'length (hours)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='lower_grade',
            field=models.IntegerField(choices=[(0, b'K'), (1, b'First'), (2, b'Second'), (3, b'Third'), (4, b'Fourth'), (5, b'Fifth'), (6, b'Sixth'), (7, b'Seventh'), (8, b'Eighth'), (9, b'Ninth'), (10, b'Tenth'), (11, b'Eleventh'), (12, b'Twelfth')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='upper_grade',
            field=models.IntegerField(choices=[(0, b'K'), (1, b'First'), (2, b'Second'), (3, b'Third'), (4, b'Fourth'), (5, b'Fifth'), (6, b'Sixth'), (7, b'Seventh'), (8, b'Eighth'), (9, b'Ninth'), (10, b'Tenth'), (11, b'Eleventh'), (12, b'Twelfth')]),
            preserve_default=True,
        ),
    ]
