import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Attendance


def _admin_only(user):
    return user.is_admin


@login_required
@user_passes_test(_admin_only)
def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Date', 'Check-in', 'Check-out'])
    for rec in Attendance.objects.select_related('karyawan').all():
        writer.writerow([
            rec.karyawan.nama,
            rec.tanggal,
            rec.jam_masuk or '-',
            rec.jam_keluar or '-',
        ])

    return response


@login_required
@user_passes_test(_admin_only)
def export_attendance_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Attendance'
    ws.append(['Employee', 'Date', 'Check-in', 'Check-out'])

    for rec in Attendance.objects.select_related('karyawan').all():
        ws.append([
            rec.karyawan.nama,
            rec.tanggal.isoformat(),
            rec.jam_masuk.strftime('%H:%M') if rec.jam_masuk else '-',
            rec.jam_keluar.strftime('%H:%M') if rec.jam_keluar else '-',
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="attendance.xlsx"'
    wb.save(response)
    return response
