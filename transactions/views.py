import random
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import  BankClient, CustomUser
from users.serializers import BankLoans
from .models import Bank, Code, Loan
from .serializers import BankSerializer, CodeSerializer, LoanSerializer, LoanCrudSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

# This is gr8

class CreateLoanView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        
        user_loans = Loan.objects.filter(client=request.data['client'])

        try:
            bank = Bank.objects.get(nom = request.data['bank'])
        except:
            return Response('bank non existant')
        if user_loans.exists():
            return Response({'error': 'You already have an active loan.'}, status=400)
        else:
            print(user_loans)
            client = BankClient.objects.get(id = request.data['client'])
            loan_amount = request.data['loan_amount']
            interest_rate = request.data['interest_rate']
            loan_start_date = request.data['loan_start_date']
            loan_end_date = request.data['loan_end_date']
            repayment_method = request.data['repayment_method']
            Loan.objects.create(
                client = client,
                loan_amount = loan_amount,
                interest_rate = interest_rate,
                bank = bank,
                loan_start_date = loan_start_date,
                loan_end_date = loan_end_date,
                repayment_method = repayment_method,
            )

        return Response({
            'Loan created successfully !'
            }, status=200)

class LoanListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        user = CustomUser.objects.get(id=id)
        query =Loan.objects.filter(client=user.id)
        # serializer=LoanSerializer(query,many=True)
        return  Response({
        "id": user.id,
        "loan_amount": query.loan_amount,
        "interest_rate": query.interest_rate,
        "loan_start_date": query.loan_start_date,
        "loan_end_date": query.loan_end_date,
        "repayment_method": query.repayment_method,
        "loan_status": query.loan_status,
        "client": query.client.id,
        "bank": query.bank.nom,
        },
        status=200)
    
class LoanView(APIView):
    def get(self,request,id):
        bank = Bank.objects.get(id=id)
        query = Loan.objects.filter(bank=bank.id)
        if query:
            serializer = LoanSerializer(query, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "No loans found for the banks."}, status=400)


@api_view(['GET'])
def getBanks(request):
    if request.method == 'GET':
        query = Bank.objects.all()
        serializer = BankSerializer(query,many=True)
        return Response(
            serializer.data
        ,status=200)
    

# this view perform all crud to the loans modele
class loanList(ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class loansCrud(RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanCrudSerializer
    
    

class ReduceLoanAmountView(APIView):
    def post(self, request, format=None):
        loans = Loan.objects.all()

        for loan in loans:
            interest_rate = loan.interest_rate
            loan_amount = loan.loan_amount
            reduced_amount = loan_amount * (1 - interest_rate)
            loan.paid_amount += loan_amount - reduced_amount
            loan.loan_amount = reduced_amount
            loan.save()

        return Response({"message": "Loan amounts reduced and paid amount updated successfully."})
    



@api_view(['POST'])
def Forget_password(request):
    phone = request.data['phone']
    try:
        user = CustomUser.objects.get(phone=phone)
    except:
        return Response({'message':'Numero de telephone incorrect',
                             'status':400,
                             })
        
    if user:
        verification_code = str(random.randint(100000, 999999))
        code = Code.objects.create(code=verification_code)
        
        
    # Serialize the new user and return the response
        serializer = CodeSerializer(code)
        return Response({'message':'Numero exsit Entrer le code ',

                             'status':200,
                             'data' : serializer.data,
                             'your code' : verification_code,
                             })
   
    # return Response({'erreur' : 'erreur'})







@api_view(['POST'])
def verification_code(request):
    data = request.data
    code = data['code']
    try:
        ver_code = Code.objects.get(code=code)
    except:
        return Response({"erreur": 'code incorrect!'}, status=400)
    if ver_code:
        ver_code.delete()
        return Response({"sucess": 'reçu avec success!','status' : 200,})
    
    else:
        return Response({'erreur': 'entrer code exist','status' : 400,})
  


