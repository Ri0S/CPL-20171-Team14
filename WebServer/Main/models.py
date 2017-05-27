# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Raspberry(models.Model):
	Ip = models.CharField(primary_key=True, max_length=20)
	auto_Blind = models.BooleanField(default=False)
	auto_Ips = models.BooleanField(default=False)
	auto_Light = models.BooleanField(default=False)

	def __str__(self):
		return self.Ip


class Sensor(models.Model):
	Ip = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
	SensorName = models.CharField(max_length=30)
	moduleNum = models.IntegerField(default=None, blank=True, null=True)
	Pin1 = models.IntegerField(default=None, blank=True, null=True)
	Pin2 = models.IntegerField(default=None, blank=True, null=True)
	Pin3 = models.IntegerField(default=None, blank=True, null=True)
	Pin4 = models.IntegerField(default=None, blank=True, null=True)

	def __str__(self):
		return self.SensorName
