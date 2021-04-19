from django.db import models


class Log(models.Model):
    ip = models.CharField(max_length=50)
    date = models.DateTimeField()
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    status_code = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
