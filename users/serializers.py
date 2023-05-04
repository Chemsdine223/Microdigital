from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from transactions.models import Loan
from users.models import  CustomUser
from django.contrib.auth.password_validation import validate_password
# from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Adminstrator
#         fields = "__all__"
        
        
class BankLoans(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class ClientRegisterSerializer(serializers.ModelSerializer):
    
    nom = serializers.CharField(
        required = True
    )
    
    # profile_image = serializers.ImageField(
    #     required = True
    # )
    
    prenom = serializers.CharField(
        required = True
    )
    
    
    # post = serializers.CharField(
    #     required = True
    # )
        
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
        model = CustomUser
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
        user = CustomUser.objects.create_user(
            phone= validated_data["phone"],
            nni= validated_data["nni"],
            nom= validated_data["nom"],
            prenom= validated_data["prenom"],
            # post= validated_data["post"],
            # profile_image= validated_data["profile_image"],

        )
        user.set_password(
            validated_data["password"]
        )
        user.save()
        return user


  