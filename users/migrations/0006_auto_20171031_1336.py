# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171023_0158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='url',
            new_name='url_template',
        ),
        migrations.AddField(
            model_name='site',
            name='domain',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]