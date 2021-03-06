# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 21:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_remove_entry_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entry',
            name='kind',
            field=models.CharField(choices=[('note', 'note'), ('article', 'article')], db_index=True, default='note', max_length=30),
        ),
    ]
