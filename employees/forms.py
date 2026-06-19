from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Leave blank if this employee should not get a login account, or if it already has one.',
    )
    password = forms.CharField(
        max_length=128, required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Only needed when creating a new login account.',
    )

    class Meta:
        model = Employee
        fields = ['nama', 'email', 'jabatan', 'tanggal_masuk', 'status_aktif']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_masuk': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user_id:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['password'].widget = forms.HiddenInput()
