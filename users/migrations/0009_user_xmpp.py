# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-06 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20171031_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='xmpp',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
