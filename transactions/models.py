from datetime import datetime
from django.db import models
from django.db import models
from django.conf import settings


class Bank(models.Model):
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.nom)
    
    
    

class Loan(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank = True)
    account_number = models.IntegerField(blank=True, null=True, unique=True)
    loan_amount = models.FloatField(max_length=255, default=0)
    interest_rate = models.FloatField(max_length=255)
    reduction_rate = models.FloatField(max_length=255)
    loan_start_date = models.DateField(default=datetime.now)
    loan_end_date = models.DateField()
    paid_amount = models.FloatField(default= 0)
    rest_to_pay = models.FloatField(default= 0,max_length=255, null=True)
    monthly_withdrawn_amount = models.FloatField(default= 0,blank=True, max_length=255, null=True)
    contract_type = models.CharField(blank=True, max_length=255, null=True)
    repayment_method = models.CharField(max_length=50)
    
    choices = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Confirmed', 'Confirmed'),
        ('Refused', 'Refused'),
    )
    
    loan_status = models.CharField(max_length=32, choices=choices, default='Pending')
    

    def __str__(self):
        return str(self.client.nom)
    


    