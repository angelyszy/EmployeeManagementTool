from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import StyledAuthenticationForm


class EmployeeLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = StyledAuthenticationForm


@login_required
def home_redirect(request):
    if request.user.is_admin:
        return redirect('employee-list')
    return redirect('attendance-checkin')
