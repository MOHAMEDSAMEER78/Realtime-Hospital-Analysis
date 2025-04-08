from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import CloudVitalSignSerializer, MedicationSerializer
from .models import CloudVitalSign, Medication
from patients.models import Patient
from . import tasks  # Import Celery tasks

@api_view(['POST'])
def receive_fog_data(request):
    print("Received data from fog server:", request.data)
    serializer = CloudVitalSignSerializer(data=request.data)
    if serializer.is_valid():
        print("Valid data received from fog")
        rfid_tag = request.data.get('rfid_tag')
        if rfid_tag:
            try:
                patient = Patient.objects.get(rfid_tag=rfid_tag)
                serializer.save(patient=patient)
                tasks.process_vital_sign_data.delay(serializer.data, patient.id)
                return Response({"message": "Fog data received and saved."}, status=status.HTTP_201_CREATED)
            except Patient.DoesNotExist:
                print(f"Patient with RFID tag '{rfid_tag}' not found.")
                return Response({"error": f"Patient with RFID tag '{rfid_tag}' not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Save without patient association
            serializer.save()
            return Response({"message": "Fog data received and saved (no patient association)."}, status=status.HTTP_201_CREATED)
    else:
        print("Invalid data received:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)