from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from transactions.models import Loan
from users.models import  CustomUser, BankClient
from django.contrib.auth.password_validation import validate_password
# from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nom']
        
        
class BankLoans(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class ClientRegisterSerializer(serializers.ModelSerializer):
    
    nom = serializers.CharField(
        required = True
    )
    
    
    prenom = serializers.CharField(
        required = True
    )
        
    nni = serializers.CharField(
        required = True,
        validators= [
            UniqueValidator(
                queryset= CustomUser.objects.all(),
                
            )
        ]
    )
    phone = serializers.IntegerField(
        required = True,
        validators= [
            UniqueValidator(
                queryset= CustomUser.objects.all(),
                
            )
        ]
    )
    
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    class Meta:
        model = BankClient
        fields = (
            "nom",
            "prenom",
            "phone",
            "nni",
            "password",
            "password2",
            
        )
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password":"passwords must match. "
                }
            )
        return attrs
    
    def create(self, validated_data):
        user = BankClient.objects.create_user(
            phone= validated_data["phone"],
            nni= validated_data["nni"],
            nom= validated_data["nom"],
            prenom= validated_data["prenom"],
        )
        user.set_password(
            validated_data["password"]
        )
        user.save()
        return user


  