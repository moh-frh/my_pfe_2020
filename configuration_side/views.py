from datetime import date

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import scapy.all as scapy
import netmiko
# Create your views here.
from configuration_side.models import Command
from reports_side.models import Report


@login_required(login_url='login')
def Configuration(request):
    ips, unans = scapy.arping("192.168.126.0/24")

    context = {'nom_page': 'configuration',
               'connected_hosts': ips,
               'report_of_today': Report.objects.filter(timestamp__gt = date.today()).count(),
               'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
               'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
               'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                   date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count()
               }

    return render(request, 'configuration.html', context)

@login_required(login_url='login')
def Commands_line(request):
    ip = request.POST.get("ip")
    device_type = request.POST.get("device_type")
    username = request.POST.get("username")
    password = request.POST.get("password")
    enable_secret_password = request.POST.get("enable_secret_password")
    # cisco_ios
    connection = netmiko.ConnectHandler(ip=ip, device_type=device_type, username=username,
                                        password=password, secret=enable_secret_password)
    # enter to enable mode
    connection.enable()
    connection.disconnect()

    request.session['ip'] = ip
    request.session['device_type'] = device_type
    request.session['username'] = username
    request.session['password'] = password
    request.session['enable_secret_password'] = enable_secret_password

    all_commands = Command.objects.filter(user=request.user.id)
    context={
        'all_commands': all_commands,

        'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
        'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
        'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
        'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count()
    }

    return render(request, 'commands_line.html', context)

@login_required(login_url='login')
def Commands(request):
    ip = request.session.get('ip')
    device_type = request.session.get('device_type')
    username = request.session.get('username')
    password = request.session.get('password')
    enable_secret_password = request.session.get('enable_secret_password')

    command = request.POST.get('command_line')

    connection = netmiko.ConnectHandler(ip=ip, device_type=device_type, username=username,
                                         password=password, secret=enable_secret_password)
    connection.enable()
    # command_result = connection.send_command(command)
    command_result = connection.send_config_set(command)

    connection.exit_config_mode()

    print(command_result)

    commandd = Command()
    commandd.command_code = command
    commandd.command_result = command_result
    # commandd.timestamp = request.POST.get("text")
    commandd.user = User.objects.get(id=request.user.id)

    commandd.save()

    all_commands = Command.objects.filter(user=request.user.id)

    context={
        'command_result': command_result,
        'command': command,
        'all_commands': all_commands,
        'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
        'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
        'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
        'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
            date_joined__gt=date.today()).count() + Command.objects.filter(timestamp__gt=date.today()).count(),

    }

    connection.exit_config_mode()
    connection.disconnect()


    return render(request, 'commands_line.html', context)