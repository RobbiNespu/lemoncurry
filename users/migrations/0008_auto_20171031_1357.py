# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20171031_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ('domain',)},
        ),
    ]
