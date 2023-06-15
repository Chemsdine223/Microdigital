# Create your views here.

import requests
import json

from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework.response import Response
from rest_framework.decorators import *

from users.models import BankClient, CustomUser
from users.serializers import ClientRegisterSerializer, ClientRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import YourModel
class BankClientUpdateView(APIView):
    def put(self, request, id):
        try:
            client = BankClient.objects.get(id=id)
        except BankClient.DoesNotExist:
            return Response({'message': 'BankClient not found.'}, status=400)

        data = request.data

        # Update the desired fields
        # if 'name' in data:
        #     client.name = data['name']

        if 'image_url' in data:
            client.image = data['image_url']

        # Save the updated instance
        client.save()

        return Response({'message': 'BankClient updated successfully.'}, status=200)



class PushNotificationView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        message = request.data.get('message')

        if not user_id or not message:
            return Response({'error': 'Missing user_id or message'}, status=400)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Basic NzE5MTEyYzktMDFiNC00Mzg4LWE2MjktYTI4ZjYyODIwNzAy',
        }
        payload = {
                    "app_id": "50c2523b-ad83-4410-8945-c16f92a18b50",
                    "contents": {
                        "en": message
                    },
                    "channel_for_external_user_ids": "push",
                    "include_external_user_ids": [
                        user_id
                    ]
                  }
        response = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return Response({'status': 'success'})
        
        else:
            return Response({'error': response.json()}, status=500)




class AuthenticatedUserData(APIView): 
    
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response(status=404)

        user_data = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'phone': user.phone,
            'nni': user.nni,
        }
        return Response(user_data)

class AuthenticatedUserDataa(APIView): 
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # user = CustomUser.objects.get(id=id)
            user = request.user
        except CustomUser.DoesNotExist:
            return Response(status=404)

        user_data = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'phone': user.phone,
            'nni': user.nni,
            'bank_id': user.bank_id.id,
            'bank_name': user.bank_id.nom,
            'telephone': user.phone
        }
        return Response(user_data)
    
    

#====================== Admins authentication: =========================#

class ClientLoginView(ObtainAuthToken):
    def post(self, request,*args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        client = CustomUser.objects.get(phone=phone)
        if client is None:
            raise AuthenticationFailed('check password')
        if client.check_password(password):
            refresh = RefreshToken.for_user(client)
            return Response({
                'id':client.id,
                'nom':client.nom,
                'prenom':client.prenom,
                'telephone':client.phone,
                'nni':client.nni,
                # 'balance':client.balance,
                # 'account_number':client.account_number,
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=Response.status_code)
        else:
            return Response({
                             'message':'error'
                            }, status= 401)  
        
        
class ClientRegisterView(generics.CreateAPIView):
    
    model = get_user_model()
    serializer_class = ClientRegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status= Response.status_code)


# ====================== Admins authentication: & Bank Loans ========================= #

class AdminLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        password = request.data['password']
        admin = CustomUser.objects.get(phone=phone)
        if admin.role == 'Manager':
            if admin.check_password(password):

                refresh = RefreshToken.for_user(admin)
                return Response({
                    'id': admin.id,
                    'nom': admin.nom,
                    'prenom': admin.prenom,
                    'telephone': admin.phone,
                    'nni': admin.nni,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'bank_id': admin.bank_id.id,
                    'bank_name': admin.bank_id.nom
                }, status=Response.status_code)
            else:
                return Response({
                                'message': 'Check your credentials'
                                }, status=401)
        else:
            raise AuthenticationFailed('Get out !')

