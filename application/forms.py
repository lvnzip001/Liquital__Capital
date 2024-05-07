from django import forms
from .models import *


class CompanyInformationForm(forms.ModelForm):
    class Meta:
        model = CompanyInformation
        fields = ['company_name', 'registration_number', 'address', 'bee_rating', 'sector', 'website']
        
        
        

        
        
class ManagingDirectorForm(forms.ModelForm):
    class Meta:
        model = ManagingDirector
        fields = ['name_surname', 'email', 'phone_number', 'id_number']


class OffTakerDetailsForm(forms.ModelForm):
    class Meta:
        model = OffTakerDetails
        fields = [
            'company_name', 'sector', 'contact_person',
            'contact_designation', 'email', 'phone_number',
            'telephone_number', 'website'
        ]

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['issue_date', 'ending_date', 'contract_number', 'description', 'value', 'payment_terms']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'ending_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InvoiceInformationForm(forms.ModelForm):
    class Meta:
        model = InvoiceInformation
        fields = ['issue_date', 'settlement_date', 'amount', 'job_description', 'payment_terms']      
        
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['description', 'amount']
        # Add form widgets if needed

class LiabilityForm(forms.ModelForm):
    class Meta:
        model = Liability
        fields = ['description', 'amount']
        # Add form widgets if needed