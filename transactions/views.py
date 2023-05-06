from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import  CustomUser
from users.serializers import BankLoans
from .models import Bank, Loan
from .serializers import BankSerializer, LoanSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.views import APIView



# from rest_framework import generics, permissions

# This is gr8
class CreateLoanView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    # serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        
        user_loans = Loan.objects.filter(client=request.user)
        try:
            bank = Bank.objects.get(nom = request.data['bank'])
        except:
            return Response('bank non existant')
        if user_loans.exists():
            return Response({'error': 'You already have an active loan.'}, status=400)
        else:
            client = CustomUser.objects.get(id = request.data['client'])
            loan_amount = request.data['loan_amount']
            interest_rate = request.data['interest_rate']
            # bank = Bank.objects.get(nom = request)
            loan_start_date = request.data['loan_start_date']
            loan_end_date = request.data['loan_end_date']
            repayment_method = request.data['repayment_method']
            loan = Loan.objects.create(
                client = client,
                loan_amount = loan_amount,
                interest_rate = interest_rate,
                bank = bank,
                loan_start_date = loan_start_date,
                loan_end_date = loan_end_date,
                repayment_method = repayment_method,
            )
            # Create the loan object
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(client=request.user)
        
        # Getting multiple loans at a time down there just in case it's needed 
        
        # loans = loan.objects.all()
        # serializer_class = LoanSerializer(loans , many = True)
        
        
        return Response({
            'Loan created successfully !'
            }, status=200)




class LoanListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        user = CustomUser.objects.get(id=id)
        query =Loan.objects.filter(client=user.id).first()
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
        "bank": query.bank.id,
        # "bank_nom":
        },status=200)
    
class LoanView(APIView):
    def get(self,request,id):
        user = CustomUser.objects.get(id=id)
        query = Loan.objects.filter(client=user.id).first()
        if query:
            serializer = LoanSerializer(query)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "No loan found for the user."}, status=400)



# class BankLoginView(ObtainAuthToken):
#     def post(self, request):
        
#         phone = request.data['phone']
#         password = request.data['password']
#         bank = Bank.objects.filter(phone=phone).first()
#         if bank is None:
#             raise AuthenticationFailed('check password')
#         if bank.check_password(password):
            
#             refresh = RefreshToken.for_user(bank)
#             return Response({
#                 'id':bank.id,
#                 'nom':bank.nom,
#                 'prenom':bank.prenom,
#                 'post':bank.post,
#                 'telephone':bank.phone,
#                 'nni':bank.nni,
#                 'refresh':str(refresh),
#                 'access':str(refresh.access_token)
#             },status=Response.status_code)
#         else:
#             return Response({
#                              'message':'Check your credentials'
#                             }, status= 401) 


@api_view(['GET'])
def getBanks(request):
    if request.method == 'GET':
        query = Bank.objects.all()
        serializer = BankSerializer(query, many = True)
        return Response(
            serializer.data
        ,status=200)




# class GetBankLoansListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self,request,id):
#         bank = Bank.objects.get(id=id)
#         query = Loan.objects.filter(bank = bank.id)
#         serializer = BankLoans(query, many = True)
#         return Response({
#             'id':bank.id,
#         })
        