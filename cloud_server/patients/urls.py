from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientList.as_view(), name='patient-list'),
    path('<int:pk>/', views.PatientDetail.as_view(), name='patient-detail'),
    path('in/', views.get_in_patients, name='in-patients'),
    path('out/', views.get_out_patients, name='out-patients'),
    path('discharge/<str:rfid_tag>/', views.discharge_patient, name='discharge-patient'),
]