import json
import logging
from time import sleep
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pysnmp.carrier.sockfix import value
from pythonping import ping
from django.contrib.auth.models import User
from pysnmp.hlapi import *
import sys, random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from reports_side.models import Report
from .forms import UserUpdateForm
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import scapy.all as scapy
from .forms import UserUpdateForm
from configuration_side.models import Command

import time
from datetime import date
from configuration_side.models import Command

from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

logger = logging.getLogger('django')



# Create your views here.
def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info('>>>>>>>>>>>>>> %s : a entrer dans son compte', username)
                return redirect('dashboard')

            else:
                messages.info(request, 'username ou password incorrecte')
                logger.warning('>>>>>>>>>>>>>> %s : a essayer de connecter', username)

                # messages.success(request, 'login sueccess')


        context={}
        return render(request, 'login.html', context)

def Get_password(request):
    print("request.POST.get('email')")
    return HttpResponse("request.POST.email_recov")

def Logout(request):
    logout(request)
    logger.info('>>>>>>>>>>>>>> un user a quitter son compte')
    return redirect('login')

def Register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                logger.info('>>>>>>>>>>>>>> le compte de %s a ete bien creer', user)
                messages.success(request, 'le compte de { '+user+' } a ete ajoute')
                print("request is_valide")
                return redirect('/login/')
            else:
                print("else")

        context = {'form':form}
        print("foorm")
        return render(request, 'register.html', context)

@login_required(login_url='login')
def Dashboard(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            user_update_form = UserUpdateForm()
            last_3_logged = User.objects.all().order_by('-last_login')[:3]
            # email_user = User.objects.get('')
            ips, unans = scapy.arping("192.168.126.0/24")

            # aaa, bbb = ips
            # print(bbb.count())
            context = {'nom_page': 'dashboard',
                       'user_update_form': user_update_form,
                       'last_3_logged': last_3_logged,
                       'connected_hosts': ips,

                       'report_of_today': Report.objects.filter(timestamp__gt = date.today()).count(),
                       'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
                       'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
                       'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                           date_joined__gt=date.today()).count() + Command.objects.filter(
                           timestamp__gt=date.today()).count(),

                       }

            return render(request, 'dashboard.html', context)
    else:
        user_update_form = UserUpdateForm()
        last_3_logged = User.objects.all().order_by('-last_login')[:3]
        # email_user = User.objects.get('')
        ips, unans = scapy.arping("192.168.126.0/24")


        context={'nom_page':'dashboard',
                 'user':user,
                 'user_update_form': user_update_form,
                 'last_3_logged': last_3_logged,
                 'connected_hosts': ips,
                 'report_of_today': Report.objects.filter(timestamp__gt = date.today()).count(),
                 'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
                 'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
                 'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                     date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count(),

                 }

        return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def Monitor(request):
    context = {'nom_page': 'monitor',
               'report_of_today': Report.objects.filter(timestamp__gt = date.today()).count(),
                 'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
                 'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
                 'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                     date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count(),
}
    return render(request, 'monitoring.html', context)

@login_required(login_url='login')
def Pre_monitor(request, ip):

    from configuration_side.models import Command
    context = {'nom_page': 'pre-monitoring',
               'net': ip,
               'report_of_today': Report.objects.filter(timestamp__gt = date.today()).count(),
                 'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
                 'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
                 'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                     date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count(),

               # 'rnd': random.randint(),
               # 'ping':ping('192.168.9.2', verbose=True),
               # 'now_time':datetime.now().strftime("%Y-%M-%d / %H:%M:%S"),
               }
    return render(request, 'pre_monitoring.html', context)

@login_required(login_url='login')
def Contact(request):
    return render(request, 'contact.html')

# @login_required(login_url='login')
def snmp_walk(host, communi, oid):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(communi),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lookupMib=False,
                              lexicographicMode=False):

        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break

        else:
            for o, result in varBinds:
                 return(result)


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def ReceiveTraps(request):
    snmpEngine = engine.SnmpEngine()

    TrapAgentAddress = '192.168.126.6';  # Trap listerner address
    Port = 162;  # trap listerner port

    print("l'ecoute le SNMP Trap sur " + TrapAgentAddress + " , Port : " + str(Port));
    print('--------------------------------------------------------------------------');
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

    # Configure community here
    config.addV1System(snmpEngine, 'my-area', 'public')

    def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
              varBinds, cbCtx):
        print("################ une nouvelle TRAP ################ ");
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

    # return render(request, "receive_traps.html")

def Test_snmp(request):
    ip = request.POST['adr_ip']
    vers = request.POST['version_snmp']
    comm = request.POST['comm_string']

    if snmp_walk(ip, comm, '1.3.6.1.2.1.1.5') is None:
        return render(request, "snmp_error.html")
    else:

        context = {'nom_periph': snmp_walk(ip, comm, '1.3.6.1.2.1.1.5'),
                   'desc_pereph': "desc",
                   'nom_page': "monitoring",
                   'sysDescr': snmp_walk(ip, comm, '1.3.6.1.2.1.1.1'),
                   'ifNumber': snmp_walk(ip, comm, '1.3.6.1.2.1.2.2.1.2'),
                   'ifSpeed': humansize(snmp_walk(ip, comm, '1.3.6.1.2.1.2.2.1.5')),
                   'ifMac': snmp_walk(ip, comm, '1.3.6.1.2.1.2.2.1.6'),

                   'cpu': snmp_walk(ip, comm, '.1.3.6.1.4.1.9.2.1.57'),
                   'free_ram': humansize(snmp_walk(ip, comm, '1.3.6.1.4.1.9.9.48.1.1.1.5')),
                   'used_ram': humansize(snmp_walk(ip, comm, '1.3.6.1.4.1.9.9.48.1.1.1.6')),
                   'number_of_users': User.objects.all().count(),

                   'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
                   'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
                   'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
                   'ip': ip,
                   # 'receive_traps': receive_traps(),
                   }


        return render(request, 'monitoring.html', context)

