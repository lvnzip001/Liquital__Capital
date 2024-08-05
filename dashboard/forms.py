from django import forms
from .models import  *

class InputForm(forms.Form):
    excel_file = forms.FileField(required=False)
    required = True

    def clean(self):
        cleaned_data = super().clean()
        excel_file = cleaned_data.get('excel_file')
        if not excel_file:
            raise forms.ValidationError("Please upload the database file first.")
        return cleaned_data


# class LoanPortfolioForm(forms.ModelForm):
#     class Meta:
#         model = LoanPortfolio
#         fields = [
#             'date', 'portfolio_pd', 'rating', 'return_on_loan_book', 
#             'return_on_cash', 'number_of_loans_advanced', 
#             'number_of_loans_outstanding', 'loan_balance', 
#             'accrued_interest', 'capital_balance', 'cash_balance', 
#             'revenue', 'outstanding_debt', 'provision_for_expected_credit_losses'
#         ]