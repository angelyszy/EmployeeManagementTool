from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from core.permissions import IsAdminRole

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [SearchFilter]
    search_fields = ['nama', 'email', 'jabatan']
