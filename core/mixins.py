from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restricts a view to admin users only, regular employees get a 403."""

    def test_func(self):
        return self.request.user.is_admin
