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
from django.urls import path, include

from authentication.views import RegisterPage
# from monitor_side.views import websock
from configuration_side.views import Configuration, Commands_line, Commands
from pages.views import Login, Dashboard, Logout, Monitor, Pre_monitor, Test_snmp, \
    Contact

from reports_side.views import CreateReport, UpdateReport, DeleteReport

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('register', RegisterPage, name='register'),


    path('dashboard', Dashboard, name='dashboard'),

    path('monitor', Monitor, name='monitor'),
    path('pre_monitor/<str:ip>', Pre_monitor, name='pre_monitor'),

    path('configuration', Configuration, name='configuration'),
    path('commands_line', Commands_line, name='commands_line'),
    path('commands', Commands, name='commands'),

    path('contact/', Contact, name='contact'),


    path('createReport/', CreateReport, name='createReport'),
    path('updateReport/<str:pk>/', UpdateReport, name='updateReport'),
    path('deleteReport/<str:pk>/', DeleteReport, name='deleteReport'),

    # path('websock', websock, name='websock'),

    path('test_snmp/', Test_snmp, name='test_snmp'),
    path('admin/log_viewer/', include('log_viewer.urls'), name="log_viewer"),

]
