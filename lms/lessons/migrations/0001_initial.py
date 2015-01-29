# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
                ('category', models.CharField(blank=True, max_length=3, choices=[(b'OFF', b'Offline'), (b'ONL', b'Online'), (b'DIS', b'Discussion')])),
                ('teaching_notes', models.TextField(blank=True)),
                ('video', models.TextField(blank=True, validators=[django.core.validators.URLValidator()])),
                ('image', models.ImageField(upload_to=b'activity_images', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rel_type', models.CharField(max_length=3, choices=[(b'SUB', b'Sub-activity'), (b'SUP', b'Super-activity'), (b'EXT', b'Extension')])),
                ('from_activity', models.ForeignKey(related_name='relationships_to', to='lessons.Activity')),
                ('to_activity', models.ForeignKey(related_name='relationships_from', to='lessons.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
                ('lower_grade', models.IntegerField(choices=[(b'0', b'K'), (b'1', b'First'), (b'2', b'Second'), (b'3', b'Third'), (b'4', b'Fourth'), (b'5', b'Fifth'), (b'6', b'Sixth'), (b'7', b'Seventh'), (b'8', b'Eighth'), (b'9', b'Ninth'), (b'10', b'Tenth'), (b'11', b'Eleventh'), (b'12', b'Twelfth')])),
                ('upper_grade', models.IntegerField(choices=[(b'0', b'K'), (b'1', b'First'), (b'2', b'Second'), (b'3', b'Third'), (b'4', b'Fourth'), (b'5', b'Fifth'), (b'6', b'Sixth'), (b'7', b'Seventh'), (b'8', b'Eighth'), (b'9', b'Ninth'), (b'10', b'Tenth'), (b'11', b'Eleventh'), (b'12', b'Twelfth')])),
                ('length_hours', models.IntegerField()),
                ('tagline', models.CharField(max_length=100, blank=True)),
                ('activities', models.ManyToManyField(related_name='curriculums', to='lessons.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('logo', models.ImageField(upload_to=b'tag_logos')),
                ('category', models.CharField(max_length=3, choices=[(b'LAN', b'Language'), (b'TEC', b'Technology'), (b'DIF', b'Difficulty'), (b'LEN', b'Length'), (b'CON', b'Concept')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='activityrelationship',
            unique_together=set([('from_activity', 'to_activity')]),
        ),
        migrations.AddField(
            model_name='activity',
            name='materials',
            field=models.ManyToManyField(to='lessons.Material', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='relationships',
            field=models.ManyToManyField(to='lessons.Activity', through='lessons.ActivityRelationship', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='resources',
            field=models.ManyToManyField(to='lessons.Resource', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tag'),
            preserve_default=True,
        ),
    ]
