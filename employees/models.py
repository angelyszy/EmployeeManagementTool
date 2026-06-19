from django.conf import settings
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profile',
    )
    nama = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    jabatan = models.CharField(max_length=100)
    tanggal_masuk = models.DateField()
    status_aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ['nama']

    def __str__(self):
        return self.nama
