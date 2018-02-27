# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-27 19:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0018_entity_user_foreignkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
