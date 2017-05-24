"""Iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Main import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^index', views.index, name='index2'),
    url(r'^about',views.about,  name='about'),
    url(r'^services/(?P<RpiIp>.*)/$', views.services, name='services'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^SensorRequest', views.SensorRequest, name='request_sensor'),
    url(r'^RaspSetting', views.RaspSetting, name="RaspSetting"),
    url(r'^Register', views.RegisterRasp, name="Register"),
    url(r'^PinSet/(?P<RpiIp>.*)/$', views.PinSetting, name="PinSet"),
    url(r'^BlindAuto/(?P<RpiIp>.*)/(?P<On>[0-9])/$', views.BlindAuto, name="BlindAuto"),
    url(r'^IpsAuto/(?P<RpiIp>.*)/(?P<On>[0-9])/$', views.IpsAuto, name="IpsAuto"),
    url(r'^LedAuto/(?P<RpiIp>.*)/(?P<On>[0-9])/$', views.LedAuto, name="LedAuto"),
    url(r'^DoorSetting/(?P<RpiIp>.*)/$', views.DoorSetting, name="DoorSetting"),
    url(r'^DoorCheck/(?P<RpiIp>.*)/$', views.DoorCheckRequest, name="DoorCheckRequest"),
    url(r'^LightRequest/(?P<RpiIp>.*)/(?P<On>[0-9])/$', views.LightRequest, name="LightRequest"),
    url(r'^IrRequest/(?P<RpiIp>.*)/(?P<DeviceName>.*)/$', views.IrRequest, name="IrRequest"),
    url(r'^CameraRequest/(?P<RpiIp>.*)/$', views.CameraRequest, name="CameraRequest"),
    url(r'^IpsBack/(?P<RpiIp>.*)/$', views.IpsBack, name="IpsBack"),
]
