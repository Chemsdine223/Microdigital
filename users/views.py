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

from users.models import CustomUser
from users.serializers import ClientRegisterSerializer, ClientRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


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
    
    



#====================== Admins authentication: =========================#

class ClientLoginView(ObtainAuthToken):
    def post(self, request):
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
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=Response.status_code)
        else:
            return Response({
                             'message':'Check your credentials'
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


#====================== Admins authentication: =========================#

class AdminLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        
        phone = request.data['phone']
        password = request.data['password']
        admin = CustomUser.objects.get(phone=phone)
        if admin.role == 'Manager':
            if admin.check_password(password):

                refresh = RefreshToken.for_user(admin)
                return Response({
                    'id':admin.id,
                    'nom':admin.nom,
                    'prenom':admin.prenom,
                    'telephone':admin.phone,
                    'nni':admin.nni,
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                },status=Response.status_code)
            else:
                return Response({
                                'message':'Check your credentials'
                                }, status= 401) 
        else:
            raise AuthenticationFailed('Get out !')

