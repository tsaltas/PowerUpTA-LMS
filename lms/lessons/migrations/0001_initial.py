# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_lesson', models.ForeignKey(related_name='from_lessons', to='lessons.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship_type', models.IntegerField(choices=[(1, b'Component'), (2, b'Extension')])),
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
                ('logo', models.ImageField(default=b'tag_logos/default.jpg', upload_to=b'tag_logos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lessonrelationship',
            name='style',
            field=models.ManyToManyField(related_name='lesson_relationships', to='lessons.RelationshipType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lessonrelationship',
            name='to_lesson',
            field=models.ForeignKey(related_name='to_lessons', to='lessons.Lesson'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lessonrelationship',
            unique_together=set([('from_lesson', 'to_lesson')]),
        ),
        migrations.AddField(
            model_name='lesson',
            name='relationships',
            field=models.ManyToManyField(to='lessons.Lesson', through='lessons.LessonRelationship'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='tags',
            field=models.ManyToManyField(to='lessons.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curriculum',
            name='lessons',
            field=models.ManyToManyField(related_name='curricula', to='lessons.Lesson'),
            preserve_default=True,
        ),
    ]
