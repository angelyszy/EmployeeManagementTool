from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from .models import Attendance


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('karyawan')
        user = self.request.user

        if not user.is_admin:
            qs = qs.filter(karyawan__user=user)

        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(karyawan__nama__icontains=query)

        tanggal = self.request.GET.get('tanggal', '').strip()
        if tanggal:
            qs = qs.filter(tanggal=tanggal)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        ctx['tanggal'] = self.request.GET.get('tanggal', '')
        return ctx


@login_required
def checkin_page(request):
    employee = getattr(request.user, 'employee_profile', None)
    if employee is None:
        messages.error(request, 'Your account is not linked to an employee record yet.')
        return redirect(reverse('home'))

    today = timezone.localdate()
    record, _ = Attendance.objects.get_or_create(karyawan=employee, tanggal=today)

    if request.method == 'POST':
        action = request.POST.get('action')
        now = timezone.localtime().time()
        if action == 'checkin' and not record.jam_masuk:
            record.jam_masuk = now
            record.save()
            messages.success(request, f'Checked in at {now.strftime("%H:%M")}.')
        elif action == 'checkout' and record.jam_masuk and not record.jam_keluar:
            record.jam_keluar = now
            record.save()
            messages.success(request, f'Checked out at {now.strftime("%H:%M")}.')
        else:
            messages.warning(request, 'That action is not available right now.')
        return redirect(reverse('attendance-checkin'))

    recent = Attendance.objects.filter(karyawan=employee).order_by('-tanggal')[:7]
    return render(request, 'attendance/checkin.html', {'record': record, 'recent': recent})
