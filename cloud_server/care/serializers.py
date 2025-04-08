from rest_framework import serializers
from .models import CloudVitalSign, Medication

class CloudVitalSignSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = CloudVitalSign
        fields = '__all__'
        read_only_fields = ('timestamp', 'patient') # Patient will be set on the server

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'