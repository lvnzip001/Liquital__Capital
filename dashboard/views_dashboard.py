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
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import re
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


def analysis_table(request):
    
    loans_df = pd.DataFrame(list(LoanDatabase.objects.all().values()))
    
    if loans_df.empty:
        messages.error(request, "Table is empty. Please upload Loans Database to generate table.")
        df_html = loans_df.to_html(classes="table datatable table-hover table-striped", index=True, border=False)
        
        return render(request, 'analysis_table.html', {'df_analysis_html': df_html})
    
    df = analysis_process(loans_df)
    
    #convert to html and remove id column
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
        
   
    df.columns = [f"{month.strftime('%b-%Y')}" for month in df.columns]

    df_html = df.to_html(classes="table datatable table-hover table-striped", index=True, border=False)
    
    df_json = df.to_json()

    # Store JSON data in session
    request.session['analysis_table'] = df_json
    
    return render(request, 'analysis_table.html', {'df_analysis_html': df_html})
    

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
    monetary_columns = ['Value of Loans Advanced','Purchase Order Financing','Invoice Discounting','Contract Financing',
                        'Value of Maturities','Black Owned','Black Female Owned','Black Female Youth Owned','Black Youth Owned','Women Owned','Youth Owned',
                        'Non-Black Owned','Suburb','Township','Rural','Government Entity','Public Listed','Private','Low Risk','Med Risk','High Risk','Eastern Cape','Western Cape',
                        'Northern Cape','North West','Gauteng','Free State','KwaZulu-Natal','Limpopo','Mpumalanga']
    for col in monetary_columns:
        summary_df[col] = summary_df[col].fillna(0).apply(lambda x: f"R {x:,.2f}")

    summary_df['Average Interest Charge'] = summary_df['Average Interest Charge'].apply(lambda x: f"{x:.2%}")
    summary_df['Average PD'] = summary_df['Average PD'].apply(lambda x: f"{x:.2%}")

    return summary_df.T  # Transpose to match your desired output format



def analysis_charts(request):
    # Retrieve the JSON data from the session

    df_json = request.session.get('analysis_table')
    
    loans_df = pd.DataFrame(list(LoanDatabase.objects.all().values()))
    
    if loans_df.empty:
            messages.error(request, "Table is empty. Please upload Loans Database to generate table.")
            df_html = loans_df.to_html(classes="table datatable table-hover table-striped", index=True, border=False)
            
            return render(request, 'analysis_table.html', {'df_analysis_html': df_html})
    

    if not df_json:
        analysis_df = analysis_process(loans_df)
    else:
        analysis_df = pd.read_json(df_json)
        
    # from the loans_df 
    number_of_loans = loans_df.shape[0]
    total_loan_amount = loans_df['loan_amount'].sum()/ 1000000
    total_loan_amount = round(total_loan_amount, 2)
    average_loan_amount = loans_df['loan_amount'].mean()/1000
    average_loan_amount = round(average_loan_amount, 1)
    total_settlement_amount = loans_df['settlement_amount'].sum()/ 1000000
    total_settlement_amount = round(total_settlement_amount, 2)
    total_settlement_count = loans_df['settlement_amount'].count()
    average_interest_charge = round(loans_df['monthly_interest_charged'].mean()*100, 2)
    jobs_created = loans_df['jobs_created'].sum()
    
    
  
    risk_allocation_chart = plot_risk_allocation(analysis_df)
    risk_proportions_chart = plot_risk_proportions(analysis_df)
    loans_vs_maturities = plot_loans_vs_maturities(analysis_df)
    loan_counts_vs_maturity_counts = plot_loan_counts_vs_maturity_counts(analysis_df)
    transaction_type_amount = plot_transaction_type_amount(analysis_df)
    transaction_type_proportions = plot_transaction_type_proportions(analysis_df)
    demographic_split_per_month = plot_demographic_split_per_month(analysis_df)
    total_demographic_split = plot_total_demographic_split(analysis_df)
    
    data = {
        "number_of_loans": number_of_loans,
        "total_loan_amount": total_loan_amount,
        "average_loan_amount": average_loan_amount,
        "total_settlement_amount": total_settlement_amount,
        "total_settlement_count": total_settlement_count,
        "average_interest_charge": average_interest_charge,
        "jobs_created": jobs_created,
        'risk_allocation_chart': pio.to_json(risk_allocation_chart),
        'risk_proportions_chart': pio.to_json(risk_proportions_chart),
        'loans_vs_maturities': pio.to_json(loans_vs_maturities),
        'loan_counts_vs_maturity_counts': pio.to_json(loan_counts_vs_maturity_counts),
        'transaction_type_amount': pio.to_json(transaction_type_amount),
        'transaction_type_proportions': pio.to_json(transaction_type_proportions),
        'demographic_split_per_month': pio.to_json(demographic_split_per_month),
        'total_demographic_split': pio.to_json(total_demographic_split)
        
    }
    
    return render(request, 'analysis_charts.html', data)
    
    
    
    
def layout_function(fig, xaxis_title, yaxis_title):
    # Update layout to make the chart more professional and modern
   
    fig.update_layout(
       # title='Risk Proportions Over Time',
        xaxis=dict(title=f'{xaxis_title}', gridcolor="lightgrey", 
                   title_font=dict(size=13, color='#012970', 
                                   family='Arial, sans-serif')),
        yaxis=dict(title=f'{yaxis_title}', 
                   gridcolor="lightgrey", 
                   title_font=dict(size=13, color='#012970', 
                                   family='Arial, sans-serif')),
        legend=dict(
                orientation="h", yanchor="top", y=1.15, xanchor="center", x=0.5
            ),
        barmode='group',  # This ensures that bars are grouped rather than stacked
        
        plot_bgcolor="white",
        shapes=[
                dict(
                    type="rect",
                    xref="paper",
                    yref="paper",
                    x0=0,
                    y0=0,
                    x1=1,
                    y1=1,
                    line=dict(color="lightgrey", width=0.5),
                )
            ],
            hoverlabel=dict(bgcolor="white", font_size=12,
                            font_family="Rockwell"),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        )
    )
    
    # Optionally, you can make the chart responsive to window and container size
    fig.update_layout(autosize=True)
    
    return fig

def plot_risk_allocation(df):
    # Assuming df contains risk allocation data with currency formatted as strings
    # Clean currency strings and convert to float for plotting
    for risk_level in ['Low Risk', 'Med Risk', 'High Risk']:
        if risk_level in df.index:
            df.loc[risk_level] = df.loc[risk_level].replace('[^\d.]', '', regex=True).astype(float)

    # Now aggregate the cleaned data across all months
    risk_data = df.loc[['Low Risk', 'Med Risk', 'High Risk']].sum(axis=1)

    # Colors for each risk level
    colors = ['#17BEBB', '#2E5266', '#FF6B6B']  # Modern color palette

    # Generate the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=risk_data.index,
        values=risk_data.values,
        marker=dict(colors=colors),
        textinfo='percent+label',
        textposition='inside',
        insidetextfont=dict(color='white', size=13),
        hole=0.35  # Optional: create a donut-like pie chart
    )])

    # Update layout for a modern and professional look
    fig.update_layout(
        
        title_font=dict(size=16, color='#012970', family='Arial, sans-serif'),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
            hoverlabel=dict(bgcolor="white", font_size=12,
                            font_family="Rockwell"))

    # Optionally, you can make the chart responsive to window and container size
    fig.update_layout(autosize=True)

    return fig

def plot_transaction_type_proportions(df):
    # Sum all months for each transaction type
    transaction_totals = df.sum(axis=1)
    transaction_types = ['Purchase Order Financing', 'Invoice Discounting', 'Contract Financing']
    values = [transaction_totals.loc[type] for type in transaction_types]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=transaction_types,
        values=values,
        marker=dict(colors=['#17BEBB', '#2E5266', '#FF6B6B']),
        textinfo='percent+label',
        insidetextfont=dict(color='white', size=14),
        hole=0.35  # Optional: create a donut-like pie chart
    )])

    fig.update_layout(
        
        title_font=dict(size=16, color='#012970', family='Arial, sans-serif'),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.3,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
        hoverlabel=dict(bgcolor="white", font_size=12,
                            font_family="Rockwell")
        )

    # Optionally, you can make the chart responsive to window and container size
    fig.update_layout(autosize=True)

    return fig

def plot_total_demographic_split(df):
    # Aggregate total loan amounts across all months for each category
    categories = ['Black Owned', 'Black Female Owned', 'Black Female Youth Owned', 
                  'Black Youth Owned', 'Women Owned', 'Youth Owned', 'Non-Black Owned']
    total_per_category = df.loc[categories].sum(axis=1)

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=total_per_category,
        marker=dict(colors=['#17BEBB', '#2E5266', '#FF6B6B', '#57CC99', '#6E85B2', '#5A189A', '#B56576']),
        textinfo='percent+label',
        insidetextfont=dict(color='white', size=13),
        hole=0.35  # Optional: create a donut-like pie chart
    )])

    fig.update_layout(
         legend=dict(
            orientation="h",
            yanchor="top",
            y=1.5,
            xanchor="center",
        ),
    )

    return fig



def plot_risk_proportions(df):
    # Assuming df contains the risk proportions data with currency formatted as strings
    # Convert formatted currency strings back to floats
    for column in df.columns:
        df[column] = df[column].replace('[^\d.]', '', regex=True).astype(float)

    # Transpose the DataFrame to get months as x-axis (dates) and risk categories as different series
    df = df.T  # Now index should be dates and columns will be risk categories
    
    colors = ['#17BEBB', '#2E5266', '#FF6B6B']  # Adjust these colors as needed

    # Create a bar for each risk category
    fig = go.Figure()
    for i, risk_category in enumerate(['Low Risk', 'Med Risk', 'High Risk']):
        fig.add_trace(go.Bar(
            x=df.index, 
            y=df[risk_category], 
            name=risk_category,
            marker_color=colors[i]  # Use the modern color palette
        ))

    # Update layout
    fig = layout_function(fig, 'Month', 'Total Amount (R)')
    
    return fig


def plot_loans_vs_maturities(df):
    # Extract the dates from the columns for the x-axis
    dates = df.columns
    
    # Extract values for Loans Advanced and Maturities from the DataFrame rows
    loans_advanced = df.loc['Value of Loans Advanced']
    maturities_value = df.loc['Value of Maturities']

    # Create figure
    fig = go.Figure()

    # Add trace for Loans Advanced
    fig.add_trace(go.Scatter(
        x=dates,
        y=loans_advanced,
        mode='lines+markers',
        name='Loans Advanced',
        line=dict(color='#17BEBB')
    ))

    # Add trace for Maturities
    fig.add_trace(go.Scatter(
        x=dates,
        y=maturities_value,
        mode='lines+markers',
        name='Maturities',
        line=dict(color='#FF6B6B')
    ))

    # Update layout
    fig = layout_function(fig, 'Month', 'Total Amount (R)')
    

    return fig

def plot_loan_counts_vs_maturity_counts(df):
    # Extract the dates from the columns for the x-axis
    dates = df.columns
    
    # Extract values for Number of Loans Advanced and Number of Maturities
    loans_count = df.loc['# of Loans Advanced']
    maturities_count = df.loc['Number of Maturities']
    # Create figure
    fig = go.Figure()

    # Add trace for Number of Loans Advanced
    fig.add_trace(go.Scatter(
        x=dates,
        y=loans_count,
        mode='lines+markers',
        name='Loans Advanced',
        line=dict(color='#2E5266')
    ))

    # Add trace for Number of Maturities
    fig.add_trace(go.Scatter(
        x=dates,
        y=maturities_count,
        mode='lines+markers',
        name='Maturities',
        line=dict(color='#FFC914')
    ))

    # Update layout
    fig = layout_function(fig, 'Month', 'Total Amount (R)')

    return fig
# of Loans Advanced

def plot_transaction_type_amount(df):
    # Assuming the DataFrame structure you provided, extracting specific rows for plotting
    purchase_order_financing = df.loc['Purchase Order Financing']
    invoice_discounting = df.loc['Invoice Discounting']
    contract_financing = df.loc['Contract Financing']

    # Dates for x-axis
    dates = df.columns

    # Create figure
    fig = go.Figure()

    # Add traces for each transaction type
    fig.add_trace(go.Bar(
        x=dates,
        y=purchase_order_financing,
        name='Purchase Order Financing',
        marker_color='#17BEBB'
    ))

    fig.add_trace(go.Bar(
        x=dates,
        y=invoice_discounting,
        name='Invoice Discounting',
        marker_color='#2E5266'
    ))

    fig.add_trace(go.Bar(
        x=dates,
        y=contract_financing,
        name='Contract Financing',
        marker_color='#FF6B6B'
    ))

    # Update layout
    fig = layout_function(fig, 'Month', 'Total Amount (R)')

    return fig

def plot_demographic_split_per_month(df):
  
    df.columns = pd.to_datetime(df.columns).strftime('%Y-%b')  # for month-year format
    #df.columns = pd.to_datetime(df.columns).to_period('M').to_timestamp()
    # Normalize each category by the total loans advanced per month to get percentages
    categories = ['Black Owned', 'Black Female Owned', 'Black Female Youth Owned', 
                  'Black Youth Owned', 'Women Owned', 'Youth Owned', 'Non-Black Owned']
    total_per_month = df.loc['Value of Loans Advanced', :]

   
    # Calculating percentages
    df_percent = df.loc[categories].div(total_per_month) * 100
    
    # Colors for the categories
    colors = ['#17BEBB', '#2E5266', '#FF6B6B', '#57CC99', '#6E85B2', '#5A189A', '#B56576']

    # Create the figure
    fig = go.Figure()
    for i, category in enumerate(categories):
        fig.add_trace(go.Bar(
            x=df_percent.columns, 
            y=df_percent.loc[category],
            name=category,
            marker_color=colors[i]
        ))

    # Update the layout for a 100% stacked bar chart
    fig.update_layout(
        barmode='relative',  # Relative barmode for 100% stacking
    )
    
    fig.update_layout(
        xaxis=dict(title='Month', 
                   gridcolor="lightgrey", 
                   tickvals=df.columns,  # Set tickvals to the exact columns (months)
                   ticktext=df.columns,  # Optional: Set custom text for each tick
                   title_font=dict(size=13, color='#012970', 
                                   family='Arial, sans-serif')),
        yaxis=dict(title='Percentage (%)', 
                   gridcolor="lightgrey", 
                   tickformat=',.2f',
                   title_font=dict(size=13, color='#012970', 
                                   family='Arial, sans-serif',
                                   )),
        legend=dict(
                orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.5
            ),
        
        plot_bgcolor="white",
        shapes=[
                dict(
                    type="rect",
                    xref="paper",
                    yref="paper",
                    x0=0,
                    y0=0,
                    x1=1,
                    y1=1,
                    line=dict(color="lightgrey", width=0.5),
                )
            ],
            hoverlabel=dict(bgcolor="white", 
                            font_size=12,
                            font_family="Rockwell"),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        )
    )
    return fig


