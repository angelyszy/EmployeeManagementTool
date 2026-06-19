from django.urls import path

from . import exports, views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee-list'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee-add'),
    path('me/', views.my_profile, name='employee-me'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee-edit'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    path('export/csv/', exports.export_employees_csv, name='employee-export-csv'),
    path('export/excel/', exports.export_employees_excel, name='employee-export-excel'),
]
