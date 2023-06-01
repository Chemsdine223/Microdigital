from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from transactions.models import Bank
from django.contrib.auth.hashers import make_password



class AccountManager(BaseUserManager):
    def create_user(self, prenom, nom, nni, phone, password=None):
        account = self.model(prenom=prenom, nom=nom, nni=nni, phone=phone)
        account.set_password(password)
        account.save(using=self._db)
        return account 

    def create_superuser(self, prenom, nom, nni, phone, password):
        user = self.create_user(prenom, nom, nni, phone, password)
        user.is_staff = True 
        user.is_superuser = True

        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('Client', 'Client'),
        ('Manager', 'Manager')
    )
    phone = models.CharField(max_length=17, unique=True)
    prenom = models.CharField(max_length=20, blank=True, null=True)
    nom = models.CharField(max_length=20, blank=True, null=True)
    nni = models.CharField(unique=True, max_length=10)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLES, default='Client', blank=True, null=True)
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["nni", "prenom", "nom"]

    
    def __str__(self):
        return str(self.prenom)

class responsable(CustomUser):
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.prenom)

class BankClient(CustomUser):
    balance = models.FloatField(max_length=255, blank=True, null=True, default=0)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    image =  models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.prenom)