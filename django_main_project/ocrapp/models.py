from django.db import models

# Create your models here.

class PingTb(models.Model):
    ping = models.CharField(max_length=255)


