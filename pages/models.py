from django.db import models

# Create your models here.
class Report(models.Model):
    type = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

