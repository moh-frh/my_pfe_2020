# Generated by Django 3.1.1 on 2020-10-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration_side', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command_result',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
