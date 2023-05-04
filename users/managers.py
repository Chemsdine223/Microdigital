from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone,password, **extra_fileds):
        
        if not phone:
            raise ValueError('phone number is required')
        
        phone = phone
        user = self.model(phone=phone,password=password ,**extra_fileds)
        user.save(self._db)
        print(user.password)
        
        return user
#         user = self.model(email=self.normalize_email(
#         email), username=username, password=password)

#   user = self.create_user(email=self.normalize_email(email), username=username, password=password)
    def create_superuser(self,phone,password = None, **extra_fields):
        user = self.create_user(
            phone,
            password,
            **extra_fields,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    
    # def create_adminstrator(self,phone,password = None, **extra_fields):
    #     user = self.create_user(

    #         phone,
    #         password,
    #         **extra_fields,
    #     )
    #     user.is_staff = False
    #     user.is_superuser = False
    #     user.save(using = self._db)
    #     return user
    
    