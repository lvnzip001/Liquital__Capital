from django.contrib import messages
from .models import LoanDatabase, LoanPortfolio
import pandas as pd
from django.shortcuts import render, redirect

# We store only the table with make up the database entires 

def loan_database_input(request, df): 
    processed_entries = 0
    for _, row in df.iterrows():
        try:
            # if _ == 3:
            #     continue
                
            # loan database will exist in the script, and all these other requirements
            LoanDatabase.objects.update_or_create(
                loan_no=int(row['Loan No.']),
                
                defaults={
                    'entity': row['Entity'],
                    'registration_number': row['Registration Number'],
                    'entity_no': int(row['Entity No.']),
                    'ownership': row['Ownership'],
                    'entity_sector': row['Entity Sector'],
                    'location': row['Location'],
                    'province': row['Province'],
                    'transaction_no': row['Transaction No.'],
                    'loan_code': row['Loan Code'],
                    'transaction_type': row['Transaction Type'],
                    'loan_amount': float(row['Loan Amount']),
                    'deployment_date': pd.to_datetime(row['Deployment Date'], errors='coerce') if pd.notna(row['Deployment Date']) and row['Deployment Date'] else None,
                    'expected_settlement_date': pd.to_datetime(row['Expected Settlement Date'], errors='coerce') if pd.notna(row['Expected Settlement Date']) and row['Expected Settlement Date'] else None,
                    'actual_settlement_date': pd.to_datetime(row['Actual Settlement Date'], errors='coerce') if pd.notna(row['Actual Settlement Date']) and row['Actual Settlement Date'] else None,
                    'settlement_amount': float(row['Settlement Amount']),
                    'admin_structuring_fee': float(row['Admin & Structuring Fee']),
                    'monthly_interest_charged': float(row['Monthly Interest Charged']),
                    'default_interest': float(row['Default Interest']),
                    'pd': float(row['PD']) if pd.notna(row['PD']) else 0,
                    'credit_rating': row['Credit Rating'],
                    'rating_code': int(row['Rating Code']),
                    'model_pricing': float(row['Model Pricing']),
                    'risk_band': row['Risk Band'],
                    'cession_of_debtors': row['Cession of Debtors'],
                    'personal_continuing_cover_surety': row['Personal Continuing Cover Surety'],
                    'cession_of_bank_accounts': row['Cession of Bank Accounts'],
                    'g_pay': row['G-PAY'],
                    'cession_of_payment': row['Cession of Payment'],
                    'cession_of_contracts': row['Cession of Contracts'],
                    'cession_of_shares': row['Cession of Shares'],
                    'value_of_ceded_collateral': float(row['Value of Ceded Collateral']),
                    'offtaker_name': row['Offtaker Name'],
                    'offtaker_type': row['Offtaker Type'],
                    'offtaker_sector': row['Offtaker Sector'],
                    'jobs_created': int(row['Jobs Created']),
                    'jobs_saved': int(row['Jobs Saved']),
                    'average_salary_per_job': float(row['Average Salary Per Job'])
                }
            )
            processed_entries += 1
        except Exception as e:
            messages.error(request, f"Error processing row {row['Loan No.']}: {str(e)}")
            continue  # You might want to handle this differently
        
    return processed_entries


def loan_portfolio_input(request, df): 
    processed_entries = 0
    for _, row in df.iterrows():
        try:
            # Helper function to clean and convert values
            def clean_value(val):
                if isinstance(val, str):
                    return float(val.replace(',', '').strip('%'))
                elif pd.notna(val):
                    return float(val)
                return 0

            LoanPortfolio.objects.update_or_create(
                date=pd.to_datetime(row['Date'], errors='coerce') if pd.notna(row['Date']) and row['Date'] else None,
                defaults={
                    'portfolio_pd': clean_value(row['Portfolio PD']),
                    'rating': row['Rating'],
                    'return_on_loan_book': clean_value(row['Return on Loan Book']),
                    'return_on_cash': clean_value(row['Return on Cash']),
                    'number_of_loans_advanced': int(row['Number of Loans Advanced']) if pd.notna(row['Number of Loans Advanced']) else 0,
                    'number_of_loans_outstanding': int(row['Number of Loans Outstanding']) if pd.notna(row['Number of Loans Outstanding']) else 0,
                    'loan_balance': clean_value(row['Loan Balance']),
                    'accrued_interest': clean_value(row['Acrued Interest']),
                    'capital_balance': clean_value(row['Capital Balance']),
                    'cash_balance': clean_value(row['Cash Balance']),
                    'revenue': clean_value(row['Revenue']),
                    'outstanding_debt': clean_value(row['Outstanding Debt']),
                    'provision_for_expected_credit_losses': clean_value(row['Provision for Expected Credit Losses']),
                }
            )
            processed_entries += 1
        except Exception as e:
            messages.error(request, f"Error processing row {row['Date']}: {str(e)}")
            continue  # You might want to handle this differently
        
    return processed_entries