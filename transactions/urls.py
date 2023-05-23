from django.urls import path
from .views import *

app_name = 'transactions'

urlpatterns = [
    path('loans/', CreateLoanView.as_view(), name='create_loan'),
    path('loans/<int:id>', LoanListView.as_view(), name='get_loans'),
    path('loanss/<int:id>', LoanView.as_view(), name='get_loans_by_bank_id'),
    path('getbanks/', getBanks, name='get_loan_by_bank'),
    path('loansCrud/<int:pk>', loansCrud.as_view(), name='crud loans'),
    path('loanList', loanList.as_view(), name='list view')
]