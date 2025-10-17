from django import forms
from django.core.validators import RegexValidator
from .models import Driver

class VehicleRegistrationForm(forms.Form):
    # Vehicle Basic Information
    plate_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'ABC 123',
            'pattern': '[A-Z]{2,3} [0-9]{3,4}'
        })
    )
    mv_file_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MV File Number'})
    )
    
    # Vehicle Identification
    cr_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificate of Registration Number'})
    )
    or_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Official Receipt Number'})
    )
    engine_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Engine Number'})
    )
    chassis_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chassis Number'})
    )
    
    # Vehicle Details
    make = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Toyota, Mitsubishi, etc.'})
    )
    model = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vios, Montero, etc.'})
    )
    series = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Series/Variant'})
    )
    year_model = forms.IntegerField(
        min_value=1900,
        max_value=2030,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'})
    )
    
    # Vehicle Classification
    body_type = forms.ChoiceField(
        choices=[
            ('', 'Select Body Type'),
            ('Sedan', 'Sedan'),
            ('SUV', 'SUV'),
            ('MPV/AUV', 'MPV/AUV'),
            ('Van', 'Van'),
            ('Pickup', 'Pickup'),
            ('Truck', 'Truck'),
            ('Bus', 'Bus'),
            ('Motorcycle', 'Motorcycle'),
            ('Other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    color = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'})
    )
    gross_vehicle_weight = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
    )
    net_capacity = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
    )
    
    # Registration Details
    date_of_issuance = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_of_expiry = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    # Fuel Type
    fuel_type = forms.ChoiceField(
        choices=[
            ('', 'Select Fuel Type'),
            ('Gasoline', 'Gasoline'),
            ('Diesel', 'Diesel'),
            ('Electric', 'Electric'),
            ('Hybrid', 'Hybrid'),
            ('LPG', 'LPG'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Ownership Details
    owner_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registered Owner Name'})
    )
    owner_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Complete address of registered owner',
            'rows': 3
        })
    )
    
    # Insurance Information
    insurance_company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance Company'})
    )
    insurance_policy_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Policy Number'})
    )
    insurance_expiry = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )



class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        exclude = ['driver_id']  # driver_id will auto-generate
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'suffix': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_type': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city_municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'license_type': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }