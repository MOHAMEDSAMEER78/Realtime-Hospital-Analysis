from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from django.utils import timezone # Import timezone
from rest_framework import generics

class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
@api_view(['GET'])
def get_in_patients(request):
    """
    Lists all currently admitted patients.
    """
    in_patients = Patient.objects.filter(discharge_date__isnull=True)
    serializer = PatientSerializer(in_patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_out_patients(request):
    """
    Lists all discharged patients.
    """
    out_patients = Patient.objects.filter(discharge_date__isnull=False)
    serializer = PatientSerializer(out_patients, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def discharge_patient(request, rfid_tag):
    """
    Discharges a patient by updating their discharge_date.
    """
    try:
        patient = Patient.objects.get(rfid_tag=rfid_tag)
        patient.discharge_date = timezone.now()  # Set discharge date to now
        patient.save()
        return Response({"message": f"Patient with RFID {rfid_tag} discharged."}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({"error": f"Patient with RFID {rfid_tag} not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def admit_patient(request, rfid_tag):
    """
    Admits a patient by setting their discharge_date to null.
    """
    try:
        patient = Patient.objects.get(rfid_tag=rfid_tag)
        patient.discharge_date = None  # Set discharge date to null
        patient.save()
        return Response({"message": f"Patient with RFID {rfid_tag} admitted."}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({"error": f"Patient with RFID {rfid_tag} not found."}, status=status.HTTP_404_NOT_FOUND)
    