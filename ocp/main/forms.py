# forms.py

from django import forms
from .models import Encadrent, Stagiaire
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator



class StagiaireForm(forms.ModelForm):
    phone_number_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Phone numbers must be 10 digits.',
    )

    cv_validator = FileExtensionValidator(allowed_extensions=['pdf'])

    class Meta:
        model = Stagiaire
        fields = ['name', 'last_name', 'cin', 'date_arr', 'date_fin', 'ecole', 'filiere', 'departement', 'encadrent', 'sujet', 'email', 'cv', 'phone']
        widgets = {
            'date_arr': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cin': forms.TextInput(attrs={'class': 'form-control'}),
            'ecole': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'filiere': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'departement': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'encadrent': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{10}', 'title': 'Please enter a valid 10-digit phone number.'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('Phone numbers must contain only digits.')
        return phone

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if not cv.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed for CV uploads.')
        return cv

class EncadrantForm(forms.ModelForm):
    class Meta:
        model = Encadrent
        fields = ['name', 'last_name', 'cin', 'departement']
        widgets = {
           
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cin': forms.TextInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('Phone numbers must contain only digits.')
        return phone
   




