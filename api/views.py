from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower()
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def _check_owner(self, doctor):
        if doctor.created_by != self.request.user:
            raise PermissionDenied("Only the creator can modify this doctor.")

    def perform_update(self, serializer):
        self._check_owner(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self._check_owner(instance)
        instance.delete()


class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = MappingSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)

    def retrieve(self, request, pk=None):
        # GET /api/mappings/<patient_id>/ -> all doctors for that patient
        qs = self.get_queryset().filter(patient_id=pk)
        return Response(self.get_serializer(qs, many=True).data)