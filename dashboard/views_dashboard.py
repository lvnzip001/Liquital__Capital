from django.shortcuts import render
import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
import pandas as pd
import io
import sqlite3
from sqlalchemy import create_engine, text
import datetime
from django.contrib import messages
# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")

def data_input(request):
    return render(request, "data_input.html")

def datatable(request):
    return render(request, "datatable.html")


def data_input(request):
    if request.method == "POST":
        form = GradeForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            excel_file = form.cleaned_data["excel_file"]
            # render a table at output, this needs to be an html
            df_html = excel_upload_view(excel_file)
            # Handle the file processing logic (e.g., using pandas to read the data and populate the Classes table)
            # Your code here
            return render(
                request,
                "data_input.html",
                {"df_html": df_html, "form": form,
                    "tbl": "LoanDatabase"},
            )
    else:
        form = GradeForm()
      
    return render(request, "data_input.html", {"form": form})


def excel_upload_view(instance):
    """
    Custom function to read the uploaded excel file in memory to view as html

    """
    uploaded_file = instance.file.read()

    # Create a BytesIO object with the file data
    file_stream = io.BytesIO(uploaded_file)

    # Read the Excel file from the BytesIO object into a DataFrame
    df = pd.read_excel(file_stream, engine="openpyxl")
    
    # Make first row the header
    df.columns = df.iloc[0]
    df = df[1:]

    # Reindex the DataFrame
    df = df.reset_index(drop=True)
    # Reorder the columns with "#" as the first column
 
    # Convert DataFrame to HTML
    df_html = df.iloc[:, 0:].to_html(
        classes="table datatable table-hover", index=False,  border= False
    )

    return df_html


# def submit_upload(request, tbl):
#     if request.method == "POST":
    
#         if "df_html" in request.POST:
#             df_html = request.POST["df_html"]
#             df = pd.read_html(df_html)[0]  # Convert HTML to DataFrame

#             # remove first column and row from df
#             df = df.iloc[:, 1:]
#             breakpoint()

#             write_df_to_sqlite(df, tbl)

#             # Return the processed DataFrame or perform further actions
#             return render(request, "success.html", context={"tbl": tbl})



    
    
def submit_upload(request, tbl):
    if request.method == "POST":
        df_html = request.POST.get("df_html")
        if not df_html:
            messages.error(request, "No data found in submission.")
            return redirect('your_form_url')  # Adjust URL as necessary

        try:
            df = pd.read_html(df_html)[0]  # Convert HTML to DataFrame
        except Exception as e:
            messages.error(request, f"Error parsing data: {str(e)}")
            return redirect('your_form_url')  # Adjust URL as necessary
       
        processed_entries = write_df_to_sqlite(request, df, tbl)
        
        messages.success(request, f"Processed {processed_entries} entries successfully.")
        return redirect("view_loans")
    else:
        # Return form page if not POST request
        return render(request, "data_input.html")
        
        
def write_df_to_sqlite(request, df, tbl):

        processed_entries = 0
        for _, row in df.iterrows():
            try:
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
                        'deployment_date': pd.to_datetime(row['Deployment Date'], errors='coerce'),
                        'expected_settlement_date': pd.to_datetime(row['Expected Settlement Date'], errors='coerce'),
                        'actual_settlement_date': pd.to_datetime(row['Actual Settlement Date'], errors='coerce'),
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


def view_loans(request):
    loans = LoanDatabase.objects.all()
    loans_df = pd.DataFrame(list(loans.values()))
    
    #convert to html and remove id column
    if 'id' in loans_df.columns:
        loans_df = loans_df.drop(columns=['id'])
    loans_df_html = loans_df.to_html(classes="table datatable table-hover", index=False, border=False)

    return render(request, 'view_loans.html', {'loans_df_html': loans_df_html})


def delete_loans(request):
    if request.method == "POST":
        if 'delete_all' in request.POST:
            LoanDatabase.objects.all().delete()
            return redirect('view_loans')
        elif 'delete' in request.POST:
            loan_no = request.POST.get('loan_no')
            # get entity
            entity = LoanDatabase.objects.get(loan_no=loan_no).entity
            LoanDatabase.objects.filter(loan_no=loan_no).delete()
            messages.success(request, f"Loan No. {loan_no} from `{entity}` was successfully remove.")
            return redirect('delete_loans')

    loans = LoanDatabase.objects.all()
    return render(request, 'view_loans_delete.html', {'loans': loans})