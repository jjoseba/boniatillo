# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from activities.models import Activity, PersonActivity

admin.site.register(Activity)
admin.site.register(PersonActivity)