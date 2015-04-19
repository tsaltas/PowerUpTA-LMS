# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0031_auto_20150419_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(unique=True, max_length=50)),
                ('number', models.IntegerField()),
                ('step_activity', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='steps',
            field=models.ManyToManyField(related_name='activities', to='lessons.Step', blank=True),
            preserve_default=True,
        ),
    ]
