from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Command(models.Model):
    command_code = models.CharField(max_length=100, null=True)
    command_result = models.TextField ()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return "command - " + str(self.id)