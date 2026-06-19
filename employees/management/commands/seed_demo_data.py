import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from attendance.models import Attendance
from employees.models import Employee

User = get_user_model()

DEMO_EMPLOYEES = [
    ('Angela Pratiwi', 'angel', 'Backend Developer'),
    ('Rizki Pratama', 'rizki', 'Frontend Developer'),
    ('Siti Nurhaliza', 'siti', 'UI/UX Designer'),
    ('Bagus Setiawan', 'bagus', 'QA Engineer'),
    ('Putri Lestari', 'putri', 'Project Manager'),
]


class Command(BaseCommand):
    help = 'Creates an admin account and a handful of demo employees with attendance history.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin12345', email='admin@example.com', role=User.Role.ADMIN)
            self.stdout.write(self.style.SUCCESS('Created admin / admin12345'))
        else:
            self.stdout.write('Admin account already exists, skipping.')

        today = timezone.localdate()

        for nama, username, jabatan in DEMO_EMPLOYEES:
            if Employee.objects.filter(email=f'{username}@example.com').exists():
                continue

            user = User.objects.create_user(username=username, password='password123', email=f'{username}@example.com', role=User.Role.EMPLOYEE)
            employee = Employee.objects.create(
                user=user,
                nama=nama,
                email=f'{username}@example.com',
                jabatan=jabatan,
                tanggal_masuk=today - timedelta(days=random.randint(60, 600)),
                status_aktif=True,
            )

            for i in range(1, 7):
                day = today - timedelta(days=i)
                if day.weekday() >= 5 or random.random() < 0.15:
                    continue
                masuk_hour = random.randint(7, 9)
                keluar_hour = masuk_hour + random.randint(7, 9)
                Attendance.objects.get_or_create(
                    karyawan=employee,
                    tanggal=day,
                    defaults={
                        'jam_masuk': f'{masuk_hour:02d}:{random.randint(0, 59):02d}',
                        'jam_keluar': f'{min(keluar_hour, 20):02d}:{random.randint(0, 59):02d}',
                    },
                )

            self.stdout.write(self.style.SUCCESS(f'Created {nama} ({username} / password123)'))

        self.stdout.write(self.style.SUCCESS('Done.'))
