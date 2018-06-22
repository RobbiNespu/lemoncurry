# Generated by Django 2.0.6 on 2018-06-12 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import randomslugfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lemonauth', '0002_delete_indieauthcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndieAuthCode',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=30, max_length=30, primary_key=True, serialize=False, unique=True)),
                ('client_id', models.URLField()),
                ('scope', models.TextField(blank=True)),
                ('redirect_uri', models.URLField()),
                ('response_type', model_utils.fields.StatusField(choices=[('id', 'id'), ('code', 'code')], default='id', max_length=100, no_check_for_status=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=30, max_length=30, primary_key=True, serialize=False, unique=True)),
                ('client_id', models.URLField()),
                ('scope', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]