from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientList.as_view(), name='patient-list'),
    path('<int:pk>/', views.PatientDetail.as_view(), name='patient-detail'),
]