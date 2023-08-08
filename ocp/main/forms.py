# forms.py

from django import forms
from .models import Stagiaire

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

    date_widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Stagiaire
        fields = '__all__'
        widgets = {
            'date_arr': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise ValidationError('Phone numbers must contain only digits.')
        return phone

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if not cv.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed for CV uploads.')
        return cv





