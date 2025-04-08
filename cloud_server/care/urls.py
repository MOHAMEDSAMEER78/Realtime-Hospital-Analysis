from django.urls import path
from . import views

websocket_urlpatterns = [
    # Define your WebSocket URL patterns in care/routing.py
]

urlpatterns = [
    path('receive_fog_data/', views.receive_fog_data, name='receive_fog_data'),
    path('vitals/', views.VitalSignList.as_view(), name='vital-sign-list'),
    path('patients/<int:patient_id>/vitals/', views.PatientVitalSignList.as_view(), name='patient-vital-sign-list'),
    path('medications/', views.MedicationList.as_view(), name='medication-list'),
    path('patients/<int:patient_id>/medications/', views.PatientMedicationList.as_view(), name='patient-medication-list'),
]
