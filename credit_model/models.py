from distutils.command.upload import upload
from pickle import TRUE
from django.db import models
from django.dispatch import receiver
import os
#from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
import hashlib
import random

# Create your models here.
#@deconstructible


class Credit_Model_Input(models.Model):
    user = models.CharField(max_length=100)
    file = models.FileField(upload_to='model_input/',null=False,blank=False)



class VariableScoring(models.Model):
    no_similar_transactions = models.IntegerField()  # No. similar transactions completed
    management_experience = models.IntegerField()  # Management Experience
    sourcing_of_service_rendered = models.CharField(max_length=50)  # Sourcing of the Service Rendered
    likelihood_of_service_delivery_delay = models.CharField(max_length=50)  # Likelihood of service delivery delay
    debt_service_cover_ratio = models.FloatField()  # Debt Service Cover Ratio
    current_ratio = models.FloatField()  # Current Ratio
    debt_ratio = models.FloatField()  # Debt ratio (D/A)
    no_cash_inflows_off_taker = models.IntegerField()  # Number of Cash inflows from off-taker
    avg_cash_inflow_loan_coverage = models.FloatField()  # Average Cash Inflow loan coverage
    past_disputes_off_taker = models.CharField(max_length=50)  # Past disputes with off-taker
    off_taker_reputational_risk = models.CharField(max_length=50)  # Off-taker reputational risk
    term_to_loan_settlement_weeks = models.IntegerField()  # Term to loan settlement (weeks)
    reputational_risk = models.CharField(max_length=50)  # Reputational risk
    availability_of_substitutes = models.IntegerField()  # Availability of substitutes
    no_suppliers_to_be_used = models.IntegerField()  # Number of suppliers to be used
    no_times_sme_used_suppliers = models.FloatField()  # Number of times the SME has used the suppliers
    unencumbered_assets_unsecured_debt = models.FloatField()  # Unencumbered Assets to the Unsecured Debt
    liquid_asset_loan_coverage_ratio = models.FloatField()  # Liquid Asset Loan Coverage Ratio
    pv_future_cash_flows_loan_coverage = models.FloatField()  # PV future Cash Flows Loan Coverage
    quality_liquid_security_loan_coverage = models.FloatField()  # Quality liquid security loan coverage
    rating = models.CharField(max_length=3)  # Rating
    rating_score = models.FloatField()  # Rating Score

    def __str__(self):
        return f"{self.rating} - {self.rating_score}"
    
    
class VariableWeighting(models.Model):
    factor_number = models.CharField(max_length=50)
    group_factor = models.CharField(max_length=100)
    factor_variable = models.CharField(max_length=100)
    purchase_order_financing = models.FloatField()
    invoice_discounting = models.FloatField()
    contract_financing = models.FloatField()

    def __str__(self):
        return f"{self.group_factor} - {self.factor_variable}"