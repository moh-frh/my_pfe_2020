
from datetime import date

from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ReportForm
# Create your views here.
from .models import Report
import logging, traceback

# import pour email sending
from django.conf import settings
from configuration_side.models import Command

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger('django')

def CreateReport(request):

    all_reports = Report.objects.filter(user = request.user.id)

    form = ReportForm()

    if request.method == 'POST':
        form = ReportForm(request.POST)

        if form.is_valid():
            report = Report()
            report.user = User.objects.get(id=request.user.id)
            report.type = request.POST.get("type")
            report.text = request.POST.get("text")
            report.save()
            print("email sending ...")

            if request.POST.get("type") == "Error":
                send_mail('PFE rapports : ',
                          'message en urgance : \n '+request.user.username+' : a creer un rapport error \n [ '+request.POST.get('text')+' ]',
                          settings.EMAIL_HOST_USER,
                          ['pfe54824@gmail.com'],
                          fail_silently=False)

            logger.info('>>>>>>>>>>>>>> %s a ajouter un rapport [%s]', request.user.username, request.POST.get('text'))
            logger.error('>>>>>>>>>>>>>> %s a ajouter un rapport [%s]', request.user.username, request.POST.get('text'))


            return redirect('createReport')


        else: logger.error('>>>>>>>>>>>>>> %s n\'a pas pu ajouter un rapport', request.user.username)


    all_reports_count = Report.objects.all().count()
    warning_reports_count = Report.objects.filter(type='Warning').count()
    error_reports_count = Report.objects.filter(type='Error').count()


    context = {'nom_page': 'gestion des rapports',
               'form': form,
               'all_reports': all_reports,
               'all_reports_count': all_reports_count,
               'warning_reports_count': warning_reports_count,
               'error_reports_count': error_reports_count,
               'ajouter_modifier': 'ajouter',

               'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
               'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
               'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
               'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                   date_joined__gt=date.today()).count() + Command.objects.filter(
                   timestamp__gt=date.today()).count(),
               }
    return render(request, 'report.html', context)

def UpdateReport(request, pk):
    report = Report.objects.get(id=pk)
    form = ReportForm(instance=report)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('createReport')
            logger.info('>>>>>>>>>>>>>> %s a modifier un rapport', request.user.username)
            redirect('createReport')
        else: logger.error('>>>>>>>>>>>>>> %s n\'a pas pu modifier le rapport', request.user.username)



    all_reports = Report.objects.filter(user = request.user.id)

    all_reports_count = Report.objects.all().count()
    warning_reports_count = Report.objects.filter(type='Warning').count()
    error_reports_count = Report.objects.filter(type='Error').count()

    context = {'nom_page': 'gestion des rapports',
               'form': form,
               'all_reports': all_reports,
               'ajouter_modifier': "modifier",
               'all_reports_count': all_reports_count,
               'warning_reports_count': warning_reports_count,
               'error_reports_count': error_reports_count,

               'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
               'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
               'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
               'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                   date_joined__gt=date.today()).count() + Command.objects.filter(
                   timestamp__gt=date.today()).count(),
               }

    return render(request, 'report.html', context)

def DeleteReport(request, pk):
    # report_to_delete = Report.objects.get(id=pk)
    # if request.method == 'POST':
    #     report_to_delete.delete()
    #     return redirect('createReport')
    # all_reports = Report.objects.all()
    # context = {'report_to_delete': report_to_delete
    #            }
    # return render(request, 'report_delete_confirm.html', context)

    report_to_delete = Report.objects.get(id=pk)
    report_to_delete.delete()
    logger.info('>>>>>>>>>>>>>> %s a supprimer un rapport', request.user.username)
    return redirect('createReport')

    all_reports = Report.objects.all()

    context = {'report_to_delete': report_to_delete,
               'report_of_today': Report.objects.filter(timestamp__gt=date.today()).count(),
               'user_of_today': User.objects.filter(date_joined__gt=date.today()).count(),
               'config_of_today': Command.objects.filter(timestamp__gt=date.today()).count(),
               'notif_count': Report.objects.filter(timestamp__gt=date.today()).count() + User.objects.filter(
                   date_joined__gt=date.today()).count() + Command.objects.filter(
                   timestamp__gt=date.today()).count(),
               }

    return render(request, 'report_delete_confirm.html', context)


