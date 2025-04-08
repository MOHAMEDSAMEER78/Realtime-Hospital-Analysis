from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import CloudVitalSignSerializer, MedicationSerializer
from .models import CloudVitalSign, Medication
from patients.models import Patient
from . import tasks  # Import Celery tasks

@api_view(['POST'])
def receive_fog_data(request):
    serializer = CloudVitalSignSerializer(data=request.data)
    print(serializer.is_valid())  # Debugging line
    if serializer.is_valid():
        print("Received data:", request.data)  # Debugging line
        rfid_tag = request.data.get('rfid_tag')
        if rfid_tag:
            try:
                patient = Patient.objects.get(rfid_tag=rfid_tag)
                serializer.save(patient=patient)
                tasks.process_vital_sign_data.delay(serializer.data, patient.id) 
                return Response({"message": "Fog data received and saved."}, status=status.HTTP_201_CREATED)
            except Patient.DoesNotExist:
                return Response({"error": f"Patient with RFID tag '{rfid_tag}' not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save() # If no RFID, save without patient (can be updated later)
            return Response({"message": "Fog data received and saved (no patient association)."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VitalSignList(generics.ListAPIView):
    queryset = CloudVitalSign.objects.all().order_by('-timestamp')
    serializer_class = CloudVitalSignSerializer

class PatientVitalSignList(generics.ListAPIView):
    serializer_class = CloudVitalSignSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return CloudVitalSign.objects.filter(patient_id=patient_id).order_by('-timestamp')

class MedicationList(generics.ListCreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class PatientMedicationList(generics.ListAPIView):
    serializer_class = MedicationSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Medication.objects.filter(patient_id=patient_id).order_by('-administration_time')
