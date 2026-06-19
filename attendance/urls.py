from django.urls import path

from . import exports, views

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance-list'),
    path('checkin/', views.checkin_page, name='attendance-checkin'),
    path('export/csv/', exports.export_attendance_csv, name='attendance-export-csv'),
    path('export/excel/', exports.export_attendance_excel, name='attendance-export-excel'),
]
