from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Report(models.Model):

    Report_types = (
        # ('Emergency', 'Emergency'),
        # ('Alert', 'Alert'),
        ('Critical', 'Critical'),
        ('Error', 'Error'),
        ('Warning', 'Warning'),
        # ('Notice', 'Notice'),
        ('Informational', 'Informational'),
        ('Debug', 'Debug'),
    )

    # sender = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True, choices=Report_types, help_text='type de rapport')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "rapport - "+str(self.id)