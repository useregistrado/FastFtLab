"""Infelplot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Infelplot.views import pdff, base, plot,fluence,zeta, radialplot,fluence1, testG, acerca, index,cedades

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fluence',fluence),
    path('fluence1',fluence1),
    path('reporte',pdff),
    path('base',base),
    path('plot',plot),
    path('radialplot',radialplot),
    path('calibracionzeta',zeta),
    path('testGalbraith',testG),
    path('acerca',acerca),
    path('',index),
    path('cedades',cedades)
]
