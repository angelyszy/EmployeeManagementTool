from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    karyawan_nama = serializers.CharField(source='karyawan.nama', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'karyawan', 'karyawan_nama', 'tanggal', 'jam_masuk', 'jam_keluar']
        read_only_fields = ['tanggal']
