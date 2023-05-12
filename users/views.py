from django.shortcuts import render

# Create your views here.
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


# Create your views here.

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
        client = CustomUser.objects.filter(phone=phone).first()
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
        admin = CustomUser.objects.filter(phone=phone).first()
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
                    'access':str(refresh.access_token), 
                    'bank_id':admin.bank_id.id,
                    'bank_name':admin.bank_id.nom
                },status=Response.status_code)
            else:
                return Response({
                                'message':'Check your credentials'
                                }, status= 401) 
        else:
            raise AuthenticationFailed('Get out !')

