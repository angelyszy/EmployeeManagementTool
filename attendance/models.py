from django.db import models
from django.utils import timezone

from employees.models import Employee


class Attendance(models.Model):
    karyawan = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    tanggal = models.DateField(default=timezone.localdate)
    jam_masuk = models.TimeField(null=True, blank=True)
    jam_keluar = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['-tanggal', '-jam_masuk']
        unique_together = ('karyawan', 'tanggal')

    def __str__(self):
        return f'{self.karyawan} - {self.tanggal}'
