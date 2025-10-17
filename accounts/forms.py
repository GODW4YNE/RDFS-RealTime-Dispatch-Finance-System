from django import forms
from django.core.validators import RegexValidator

class DriverRegistrationForm(forms.Form):
    # Personal Information
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
    
    # Address (Philippine format)
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
    
    # Driver's License Information (Philippine format)
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
    
    # Additional Information
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