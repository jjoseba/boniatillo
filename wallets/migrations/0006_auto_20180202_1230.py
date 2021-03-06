# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-02 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0005_transactionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionlog',
            name='related',
            field=models.TextField(blank=True, null=True, verbose_name='Concepto'),
        ),
        migrations.AddField(
            model_name='transactionlog',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallets.Transaction'),
        ),
    ]
