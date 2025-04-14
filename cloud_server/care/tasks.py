from celery import shared_task
from .models import CloudVitalSign
from django.utils import timezone
import json

@shared_task
def process_vital_sign_data(vital_sign_data, patient_id):
    """
    Example Celery task to perform further processing on vital sign data.
    """
    print(f"Processing vital sign data for patient ID: {patient_id}")
    # You can add more complex analysis or actions here, e.g.,
    # - Checking for critical thresholds
    # - Logging data for long-term analysis
    # - Triggering alerts
    print(f"Received vital sign data: {vital_sign_data}")
    temperature = vital_sign_data.get('temperature')
    if temperature is not None and temperature > 38:
        print(f"WARNING: High temperature detected for patient ID: {patient_id}, Temperature: {temperature}")
