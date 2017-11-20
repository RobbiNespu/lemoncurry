# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0006_auto_20171102_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='cite',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='kind',
            field=models.CharField(choices=[('note', 'note'), ('article', 'article'), ('photo', 'photo'), ('reply', 'reply'), ('like', 'like'), ('repost', 'repost')], db_index=True, default='note', max_length=30),
        ),
    ]