import json

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pysnmp.carrier.sockfix import value
from pythonping import ping

from pysnmp.hlapi import *
import sys, random


import platform    # For getting the operating system name
import subprocess  # For executing a shell command

from datetime import datetime

# Create your views here.
def Login(request):
    context={}
    return render(request, 'login.html', context)

def Logout(request):
    logout(request)
    return redirect('login')

def Register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'register.html', context)

def Dashboard(request):
    context={'nom_page':'dashboard'}
    return render(request, 'dashboard.html', context)

def Monitor(request):
    context = {'nom_page': 'monitor'}
    return render(request, 'monitoring.html', context)

# def ping(host):
#     """
#     Returns True if host (str) responds to a ping request.
#     Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
#     """
#
#     # Option for the number of packets as a function of
#     # param = '-n' if platform.system().lower()=='windows' else '-c'
#     #
#     # # Building the command. Ex: "ping -c 1 google.com"
#     # command = ['ping', param, '1', host]
#     #
#     # return subprocess.call(command) == 0
#     ping(host, verbose=True)


    # return subprocess.call(command)



def Pre_monitor(request):

    context = {'nom_page': 'pre-monitoring',
               # 'ping':ping('192.168.9.2', verbose=True),
               'now_time':datetime.now().strftime("%Y-%M-%d / %H:%M:%S")}
    
    return render(request, 'pre_monitoring.html', context)


def Configuration(request):
    context = {'nom_page': 'configuration'}

    return render(request, 'dashboard.html', context)

def Report(request):
    context = {'nom_page': 'raport'}

    return render(request, 'report.html', context)

def Contact(request):
    return render(request, 'contact.html')


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


def Test_snmp(request):
    ip = request.POST['adr_ip']
    vers = request.POST['version_snmp']
    comm = request.POST['comm_string']


    # context = {'nom_periph' : snmp_walk(ip, comm, '1.3.6.1.2.1.1.5'),
    #            'desc_pereph' : snmp_walk(ip, comm, '1.3.6.1.2.1.1.1'),
    #            'bw':rand(),
    #            'nom_page':"monitoring"}

    context = {'nom_periph': "nom",
               'desc_pereph': "desc",
               'nom_page': "monitoring",
               'bw': random.uniform(0, 10),
               }



    return render(request, 'monitoring.html', context)

    # snmp_walk('192.168.126.1', '1.3.6.1.2.1.1.1')

    # process = snmp_walk('192.168.126.1', '1.3.6.1.2.1.1.1')

# def Contact(request):
#     context = {'nom_page': 'contact'}
#
#     return render(request, 'contact.html', context)
