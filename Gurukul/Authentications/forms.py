from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from Authentications.models import Profile

# -----------------------------
# Registration Form
# -----------------------------
class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match.")

        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as e:
                self.add_error('password', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Using email as username
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create associated Profile
            Profile.objects.get_or_create(user=user, full_name=self.cleaned_data['name'])
        return user


# -----------------------------
# Password Reset Form
# -----------------------------
class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your@example.com', 'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account is associated with this email address.")
        return email


# -----------------------------
# Password Change Form
# -----------------------------
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Old Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_('New Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_('Confirm Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
