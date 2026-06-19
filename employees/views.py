from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin

from .forms import EmployeeForm
from .models import Employee

User = get_user_model()


class EmployeeListView(AdminRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(
                Q(nama__icontains=query) | Q(email__icontains=query) | Q(jabatan__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


@login_required
def my_profile(request):
    employee = getattr(request.user, 'employee_profile', None)
    if employee is None:
        messages.error(request, 'Your account is not linked to an employee record yet.')
        return redirect('home')
    return redirect('employee-detail', pk=employee.pk)


class EmployeeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def test_func(self):
        employee = self.get_object()
        return self.request.user.is_admin or employee.user_id == self.request.user.id


class EmployeeCreateView(AdminRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        if username and password:
            user = User.objects.create_user(username=username, password=password, email=self.object.email)
            self.object.user = user
            self.object.save()
            messages.success(self.request, f'Employee added, login account "{username}" created.')
        else:
            messages.success(self.request, 'Employee added.')
        return response


class EmployeeUpdateView(AdminRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Employee updated.')
        return response


class EmployeeDeleteView(AdminRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employee removed.')
        return super().form_valid(form)
