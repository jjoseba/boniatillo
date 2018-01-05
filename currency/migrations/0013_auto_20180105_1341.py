# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-05 13:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0012_auto_20180105_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='rel_transaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='wallet_from',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='wallet_to',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]
