# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalapp', '0005_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_from',
            new_name='from_date',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_headline',
            new_name='headline',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_to',
            new_name='to_date',
        ),
        migrations.AddField(
            model_name='project',
            name='ptype',
            field=models.CharField(choices=[(b'Self', b'Self'), (b'Institute', b'Institute')], default=b'Self', max_length=50),
        ),
    ]