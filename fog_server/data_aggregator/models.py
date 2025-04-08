from django.db import models

# Create your models here.
class EdgeData(models.Model):
    rfid_tag = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)