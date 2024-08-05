import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tabulate import tabulate

def calculate_amortization_schedule(principal, annual_interest_rate, total_term_months, total_monthly_payment, other_fees, start_date, lump_sum_payments):
    monthly_interest_rate = annual_interest_rate / 12
    
    # The actual monthly loan payment excluding other fees
    loan_monthly_payment = total_monthly_payment - other_fees
    
    schedule = []
    remaining_balance = principal
    current_date = datetime.strptime(start_date, '%Y-%m-%d')

    for month in range(1, total_term_months + 1):
        if month in lump_sum_payments:
            remaining_balance -= lump_sum_payments[month]
            if remaining_balance <= 0:
                remaining_balance = 0
                break

        # Check if the current month is January
        if current_date.month == 1:
            # Only pay interest
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = 0
        else:
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = loan_monthly_payment - interest_payment
        
        remaining_balance -= principal_payment

        schedule.append({
            'Month': month,
            'Date': current_date.strftime('%Y-%m-%d'),
            'Total Monthly Payment': round(total_monthly_payment if current_date.month != 1 else interest_payment + other_fees, 2),
            'Interest Payment': round(interest_payment, 2),
            'Principal Payment': round(principal_payment, 2),
            'Other Fees': round(other_fees, 2),
            'Remaining Balance': round(remaining_balance, 2)
        })

        if remaining_balance <= 0:
            break
        
        # Move to the next month
        next_month = current_date.month % 12 + 1
        current_date = current_date.replace(month=next_month, day=1)
        if next_month == 1:
            current_date = current_date.replace(year=current_date.year + 1)

    return pd.DataFrame(schedule)

# Loan details
principal = 45456
annual_interest_rate = 28.75 / 100
total_term_months = 65
total_monthly_payment = 1730
other_fees = 220
start_date = '2023-06-01'
lump_sum_payments = {11:20000}  # Example lump sum payments

# Calculate schedule
amortization_schedule = calculate_amortization_schedule(principal, annual_interest_rate, total_term_months, total_monthly_payment, other_fees, start_date, lump_sum_payments)

# Display schedule using tabulate
print(tabulate(amortization_schedule, headers='keys', tablefmt='psql'))

# Save to CSV and Excel
amortization_schedule.to_csv('amortization_schedule.csv', index=False)
amortization_schedule.to_excel('amortization_schedule.xlsx', index=False)
