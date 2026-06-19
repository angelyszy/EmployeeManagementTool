import json
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from attendance.models import Attendance
from core.mixins import AdminRequiredMixin
from django.views.generic import TemplateView
from employees.models import Employee


class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        by_position = (
            Employee.objects.values('jabatan').annotate(total=Count('id')).order_by('-total')
        )

        today = timezone.localdate()
        start = today - timedelta(days=6)
        daily_counts = (
            Attendance.objects.filter(tanggal__gte=start, tanggal__lte=today)
            .values('tanggal')
            .annotate(total=Count('id'))
        )
        counts_by_date = {row['tanggal']: row['total'] for row in daily_counts}
        attendance_labels = []
        attendance_values = []
        for i in range(7):
            day = start + timedelta(days=i)
            attendance_labels.append(day.strftime('%d %b'))
            attendance_values.append(counts_by_date.get(day, 0))

        ctx['position_labels'] = json.dumps([row['jabatan'] for row in by_position])
        ctx['position_values'] = json.dumps([row['total'] for row in by_position])
        ctx['attendance_labels'] = json.dumps(attendance_labels)
        ctx['attendance_values'] = json.dumps(attendance_values)
        ctx['total_employees'] = Employee.objects.count()
        ctx['active_employees'] = Employee.objects.filter(status_aktif=True).count()
        ctx['today_checkins'] = Attendance.objects.filter(tanggal=today, jam_masuk__isnull=False).count()

        return ctx
