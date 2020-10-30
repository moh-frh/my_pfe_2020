from django.contrib import admin

# Register your models here.
# from pages.models import Report
from reports_side.models import Report

admin.site.register(Report)

# ou bien :
#
# @admin.register(Report)
# class ReportAdmin(admin.ModelAdmin):
#     fields = ['type']
#     # list_display = ['type']
#     list_filter = ['type']
#     search_fields = ['description']