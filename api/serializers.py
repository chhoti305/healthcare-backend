from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Patient, Doctor, PatientDoctorMapping


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def create(self, data):
        return User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            first_name=data["name"],
        )


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("created_by",)


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = "__all__"

    def validate_patient(self, patient):
        if patient.created_by != self.context["request"].user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return patient