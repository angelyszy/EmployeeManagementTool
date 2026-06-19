from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import home_redirect
from attendance.api_views import AttendanceViewSet
from employees.api_views import EmployeeViewSet

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='api-employee')
router.register('attendance', AttendanceViewSet, basename='api-attendance')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]
