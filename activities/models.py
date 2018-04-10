# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models


class Activity(models.Model):

    name = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    type_activity = models.CharField(null=True, blank=True, verbose_name='Tipo', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['name']

    def __unicode__(self):
        return self.name if self.name else ''
