# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

from currency.models import Person


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


class PersonActivity(models.Model):

    activity = models.ForeignKey(Activity, related_name='user_activity', verbose_name='Actividad')
    person = models.ForeignKey(Person, null=True, related_name='activities', verbose_name='Persona que realiza la actividad')
    day = models.DateField(verbose_name='Día de tarea', default=datetime.now)
    time_spent = models.TimeField(default=0, verbose_name='Tiempo empleado')

    class Meta:
        verbose_name = 'Actividad realizada'
        verbose_name_plural = 'Actividades realizadas'
        ordering = ['day']

    def __unicode__(self):
        return str(self.person) + ' - ' + str(self.activity)
