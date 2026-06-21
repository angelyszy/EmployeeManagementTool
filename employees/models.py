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
    nama = models.CharField(max_length=150, verbose_name='Name')
    email = models.EmailField(unique=True, verbose_name='Email')
    jabatan = models.CharField(max_length=100, verbose_name='Position')
    tanggal_masuk = models.DateField(verbose_name='Join Date')
    status_aktif = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        ordering = ['nama']

    def __str__(self):
        return self.nama
