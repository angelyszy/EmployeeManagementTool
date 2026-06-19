from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        EMPLOYEE = 'employee', 'Employee'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.EMPLOYEE)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.Role.ADMIN

    def __str__(self):
        return self.username
