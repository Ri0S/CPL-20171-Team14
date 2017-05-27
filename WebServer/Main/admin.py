# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Main.models import Raspberry, Sensor
# Register your models here.

admin.site.register(Raspberry)
admin.site.register(Sensor)
