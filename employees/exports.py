import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Employee


def _admin_only(user):
    return user.is_admin


@login_required
@user_passes_test(_admin_only)
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Position', 'Join Date', 'Active'])
    for emp in Employee.objects.all():
        writer.writerow([emp.nama, emp.email, emp.jabatan, emp.tanggal_masuk, 'Yes' if emp.status_aktif else 'No'])

    return response


@login_required
@user_passes_test(_admin_only)
def export_employees_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Employees'
    ws.append(['Name', 'Email', 'Position', 'Join Date', 'Active'])

    for emp in Employee.objects.all():
        ws.append([emp.nama, emp.email, emp.jabatan, emp.tanggal_masuk.isoformat(), 'Yes' if emp.status_aktif else 'No'])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
    wb.save(response)
    return response
