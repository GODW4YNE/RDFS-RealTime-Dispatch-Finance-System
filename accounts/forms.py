from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# ✅ DRIVER REGISTRATION FORM (unchanged)
class DriverRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    suffix = forms.ChoiceField(
        choices=[('', 'Select Suffix'), ('Jr.', 'Jr.'), ('Sr.', 'Sr.'), ('II', 'II'), ('III', 'III')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+639171234567'. Up to 15 digits allowed."
    )
    mobile_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567',
            'pattern': '^(\\+63|0)9\\d{9}$'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )

    # Address
    house_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Bldg No.'})
    )
    street = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    barangay = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay'})
    )
    city_municipality = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Municipality'})
    )
    province = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'})
    )
    zip_code = forms.CharField(
        max_length=4,
        validators=[RegexValidator(regex='^[0-9]{4}$', message='Enter a valid 4-digit ZIP code')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code', 'pattern': '[0-9]{4}'})
    )

    # License Information
    license_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N01-23-456789'})
    )
    license_expiry = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    license_type = forms.ChoiceField(
        choices=[
            ('', 'Select License Type'),
            ('Student', 'Student Permit'),
            ('Non-Professional', 'Non-Professional'),
            ('Professional', 'Professional'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Additional Info
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    birth_place = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place of Birth'})
    )
    blood_type = forms.ChoiceField(
        choices=[
            ('', 'Select Blood Type'),
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Emergency Contact
    emergency_contact_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'})
    )
    emergency_contact_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567',
            'pattern': '^(\\+63|0)9\\d{9}$'
        })
    )
    emergency_contact_relationship = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'})
    )


# ✅ UPDATED ROLE-AWARE CUSTOM USER CREATION FORM (Admin + Staff)
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff_admin', 'Staff Admin'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Account Role",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Hide the Admin role if a staff_admin is creating a user."""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and getattr(user, 'role', '') == 'staff_admin':
            self.fields['role'].choices = [('staff_admin', 'Staff Admin')]

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        # ✅ Automatically assign correct privileges
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'staff_admin':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


# ✅ USER EDIT FORM
class CustomUserEditForm(UserChangeForm):
    password = None  # hide password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']
