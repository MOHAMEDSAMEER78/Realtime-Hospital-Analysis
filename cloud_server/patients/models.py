from django.db import models

class Patient(models.Model):
    rfid_tag = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name