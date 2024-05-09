from django import forms
from .models import  *

class GradeForm(forms.Form):
    excel_file = forms.FileField(required=False)
    required = True

    def clean(self):
        cleaned_data = super().clean()
        excel_file = cleaned_data.get('excel_file')
        if not excel_file:
            raise forms.ValidationError("Please upload the database file first.")
        return cleaned_data
