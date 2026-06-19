from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'nama', 'email', 'jabatan', 'tanggal_masuk', 'status_aktif']
