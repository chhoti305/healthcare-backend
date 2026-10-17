from django.conf import settings
from django.db import models


class Patient(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients")
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Doctor(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctors")
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    experience_years = models.PositiveIntegerField(default=0)


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="mappings")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("patient", "doctor")