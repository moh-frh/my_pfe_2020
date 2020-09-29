"""my_pfe_2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from pages.views import Login, Register, Dashboard, Logout, Monitor, Configuration, Pre_monitor, Report, Test_snmp, \
    Contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('register', Register, name='register'),
    path('', Dashboard, name='dashboard'),

    path('monitor', Monitor, name='monitor'),
    path('pre_monitor', Pre_monitor, name='pre_monitor'),

    path('configuration', Configuration, name='configuration'),
    path('report/', Report, name='report'),
    path('contact/', Contact, name='contact'),
    path('test_snmp/', Test_snmp, name='test_snmp'),

]
