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


def analysis_process(df):
    # Convert 'deployment_date' to datetime
    df['deployment_date'] = pd.to_datetime(df['deployment_date'])
    df['month_year'] = df['deployment_date'].dt.to_period('M')
    
    # Initialize the DataFrame for summarization
    summary_df = pd.DataFrame(index=pd.period_range(df['deployment_date'].min(), df['deployment_date'].max(), freq='M'))
    
    # Financial categories
    summary_df['# of Loans Advanced'] = df.groupby('month_year').size()
    summary_df['Value of Loans Advanced'] = df.groupby('month_year')['loan_amount'].sum().fillna(0)
    summary_df['Purchase Order Financing'] = df[df['transaction_type'] == 'Purchase Order Financing'].groupby('month_year')['loan_amount'].sum()
    summary_df['Invoice Discounting'] = df[df['transaction_type'] == 'Invoice Discounting'].groupby('month_year')['loan_amount'].sum()
    summary_df['Contract Financing'] = df[df['transaction_type'] == 'Contract Financing'].groupby('month_year')['loan_amount'].sum()
    summary_df['Average Interest Charge'] = df.groupby('month_year')['monthly_interest_charged'].mean().fillna(0)
    summary_df['Number of Maturities'] = df.groupby('month_year')['settlement_amount'].count()
    summary_df['Value of Maturities'] = df.groupby('month_year')['settlement_amount'].sum()
    summary_df['Average PD'] = df.groupby('month_year')['pd'].mean().fillna(0)
    
    summary_df['Mpumalanga'] = df[df['province'] == 'Mpumalanga'].groupby('month_year')['loan_amount'].sum()
    summary_df['Limpopo'] = df[df['province'] == 'Limpopo'].groupby('month_year')['loan_amount'].sum()
    summary_df['KwaZulu-Natal'] = df[df['province'] == 'KwaZulu-Natal'].groupby('month_year')['loan_amount'].sum()
    summary_df['Free State'] = df[df['province'] == 'Free State'].groupby('month_year')['loan_amount'].sum()
    summary_df['Gauteng'] = df[df['province'] == 'Gauteng'].groupby('month_year')['loan_amount'].sum()
    summary_df['North West'] = df[df['province'] == 'North West'].groupby('month_year')['loan_amount'].sum()
    summary_df['Northern Cape'] = df[df['province'] == 'Northern Cape'].groupby('month_year')['loan_amount'].sum()
    summary_df['Western Cape'] = df[df['province'] == 'Western Cape'].groupby('month_year')['loan_amount'].sum()
    summary_df['Eastern Cape'] = df[df['province'] == 'Eastern Cape'].groupby('month_year')['loan_amount'].sum()
    summary_df['Low Risk'] = df[df['risk_band'] == 'Low Risk'].groupby('month_year')['loan_amount'].sum()
    summary_df['Med Risk'] = df[df['risk_band'] == 'Med Risk'].groupby('month_year')['loan_amount'].sum()
    summary_df['High Risk'] = df[df['risk_band'] == 'High Risk'].groupby('month_year')['loan_amount'].sum()
    summary_df['Government Entity'] = df[df['offtaker_type'] == 'Government Entity'].groupby('month_year')['loan_amount'].sum()
    summary_df['Public Listed'] = df[df['offtaker_type'] == 'Public Listed'].groupby('month_year')['loan_amount'].sum()
    summary_df['Private'] = df[df['offtaker_type'] == 'Private'].groupby('month_year')['loan_amount'].sum()
    summary_df['Black Owned'] = df[df['ownership'] == 'Black Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Black Female Owned'] = df[df['ownership'] == 'Black Female Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Black Female Youth Owned'] = df[df['ownership'] == 'Black Female Youth Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Black Youth Owned'] = df[df['ownership'] == 'Black Youth Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Women Owned'] = df[df['ownership'] == 'Women Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Youth Owned'] = df[df['ownership'] == 'Youth Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Non-Black Owned'] = df[df['ownership'] == 'Non-Black Owned'].groupby('month_year')['loan_amount'].sum()
    summary_df['Suburb'] = df[df['location'] == 'Suburb'].groupby('month_year')['loan_amount'].sum()
    summary_df['Township'] = df[df['location'] == 'Township'].groupby('month_year')['loan_amount'].sum()
    summary_df['Rural'] = df[df['location'] == 'Rural'].groupby('month_year')['loan_amount'].sum()
    
    
    
    

   

    # Formatting outputs for currency and percentage
    monetary_columns = ['Value of Loans Advanced','Purchase Order Financing','Invoice Discounting','Contract Financing','Number of Maturities',
                        'Value of Maturities','Black Owned','Black Female Owned','Black Female Youth Owned','Black Youth Owned','Women Owned','Youth Owned',
                        'Non-Black Owned','Suburb','Township','Rural','Government Entity','Public Listed','Private','Low Risk','Med Risk','High Risk','Eastern Cape','Western Cape',
                        'Northern Cape','North West','Gauteng','Free State','KwaZulu-Natal','Limpopo','Mpumalanga']
    for col in monetary_columns:
        summary_df[col] = summary_df[col].fillna(0).apply(lambda x: f"R {x:,.2f}")

    summary_df['Average Interest Charge'] = summary_df['Average Interest Charge'].apply(lambda x: f"{x:.2%}")
    summary_df['Average PD'] = summary_df['Average PD'].apply(lambda x: f"{x:.2%}")

    return summary_df.T  # Transpose to match your desired output format

  
    
    
def analysis_table(request):
    
    loans_df = pd.DataFrame(list(LoanDatabase.objects.all().values()))
    
    df = analysis_process(loans_df)
    
    #convert to html and remove id column
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    df_html = df.to_html(classes="table datatable table-hover table-striped", index=True, border=False)
    
    return render(request, 'analysis_table.html', {'df_analysis_html': df_html})
    


# of Loans Advanced

