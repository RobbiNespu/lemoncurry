# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 03:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_syndication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='summary',
        ),
    ]
