# Generated by Django 3.1.1 on 2020-10-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports_side', '0004_report_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.CharField(choices=[('critique', 'critique'), ('danger', 'danger')], help_text='type de rapport', max_length=100, null=True),
        ),
    ]
