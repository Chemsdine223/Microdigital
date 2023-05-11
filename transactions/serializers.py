from rest_framework import serializers
from .models import Bank, Loan


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'client', 'loan_amount', 'interest_rate', 'loan_status', 'loan_start_date', 'loan_end_date', 'repayment_method','bank']
