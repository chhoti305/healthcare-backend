from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, LoginView, PatientViewSet, DoctorViewSet, MappingViewSet,
)

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("", include(router.urls)),
]