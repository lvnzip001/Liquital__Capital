from django.db import models

class LoanDatabase(models.Model):
    loan_no = models.IntegerField()
    entity = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50)
    entity_no = models.IntegerField()
    ownership = models.CharField(max_length=100)
    entity_sector = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    transaction_no = models.CharField(max_length=50)
    loan_code = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=100)
    loan_amount = models.FloatField()
    deployment_date = models.DateField(null=True, blank=True)
    expected_settlement_date = models.DateField(null=True, blank=True)
    actual_settlement_date = models.DateField(null=True, blank=True)
    settlement_amount = models.FloatField()
    admin_structuring_fee = models.FloatField()
    monthly_interest_charged = models.FloatField()
    default_interest = models.FloatField()
    pd = models.FloatField()
    credit_rating = models.CharField(max_length=50)
    rating_code = models.IntegerField()
    model_pricing = models.FloatField()
    risk_band = models.CharField(max_length=100)
    cession_of_debtors = models.CharField(max_length=3)
    personal_continuing_cover_surety = models.CharField(max_length=3)
    cession_of_bank_accounts = models.CharField(max_length=3)
    g_pay = models.CharField(max_length=3)
    cession_of_payment = models.CharField(max_length=3)
    cession_of_contracts = models.CharField(max_length=3)
    cession_of_shares = models.CharField(max_length=3)
    value_of_ceded_collateral = models.FloatField()
    offtaker_name = models.CharField(max_length=100)
    offtaker_type = models.CharField(max_length=100)
    offtaker_sector = models.CharField(max_length=100)
    jobs_created = models.IntegerField()
    jobs_saved = models.IntegerField()
    average_salary_per_job = models.FloatField()

    def __str__(self):
        return f"{self.entity} - {self.transaction_no}"
    
    
class LoanPortfolio(models.Model):
    date = models.DateField()
    portfolio_pd = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.CharField(max_length=10)
    return_on_loan_book = models.DecimalField(max_digits=5, decimal_places=2)
    return_on_cash = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_loans_advanced = models.IntegerField()
    number_of_loans_outstanding = models.IntegerField()
    loan_balance = models.DecimalField(max_digits=15, decimal_places=2)
    accrued_interest = models.DecimalField(max_digits=15, decimal_places=2)
    capital_balance = models.DecimalField(max_digits=15, decimal_places=2)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_debt = models.DecimalField(max_digits=15, decimal_places=2)
    provision_for_expected_credit_losses = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Loan Portfolio as of {self.date}"
    
    
