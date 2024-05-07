from django.db import models

#! Section 1 Company Information
class CompanyInformation(models.Model):
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    address = models.TextField()
    bee_rating = models.CharField(max_length=50)
    sector = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)  # Website is optional

    def __str__(self):
        return self.company_name
    
#! Section 2 Company Contact Information
class ManagingDirector(models.Model):
    name_surname = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name_surname

#! Off-Taker Details
class OffTakerDetails(models.Model):
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=255)
    contact_designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)  # Optional
    website = models.URLField(blank=True, null=True)  # Optional

    def __str__(self):
        return self.company_name
    
#! Purchase Order Information
class Contract(models.Model):
    issue_date = models.DateField()
    ending_date = models.DateField()
    contract_number = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.TextField()

    def __str__(self):
        return self.contract_number
    
#! InvoiceInformation
class InvoiceInformation(models.Model):
    issue_date = models.DateField()
    settlement_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    job_description = models.TextField()
    payment_terms = models.TextField()

    def __str__(self):
        return f"Invoice issued on {self.issue_date}"

#! Section 12 Director(s) Asset & Liability Statement
class Asset(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields as needed

class Liability(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields as needed

