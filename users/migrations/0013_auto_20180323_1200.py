# Generated by Django 2.0.3 on 2018-03-23 01:00

import computed_property.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20180129_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_md5',
            field=computed_property.fields.ComputedCharField(compute_from='calc_email_md5', default='', editable=False, max_length=32, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_sha256',
            field=computed_property.fields.ComputedCharField(compute_from='calc_email_sha256', default='', editable=False, max_length=64, unique=True),
        ),
    ]
