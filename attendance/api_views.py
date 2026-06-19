from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['karyawan__nama']

    def get_queryset(self):
        qs = Attendance.objects.select_related('karyawan').all()
        if self.request.user.is_admin:
            return qs
        return qs.filter(karyawan__user=self.request.user)
