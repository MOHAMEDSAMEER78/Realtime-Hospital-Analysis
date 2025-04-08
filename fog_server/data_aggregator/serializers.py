from rest_framework import serializers
from .models import EdgeData

class EdgeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeData
        fields = ['rfid_tag', 'temperature', 'heart_rate', 'timestamp']
        read_only_fields = ('timestamp',) # Timestamp is set by the server