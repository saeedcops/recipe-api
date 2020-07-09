from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**exta_fields):
        """This method is to create user"""
        if not email:
            raise ValueError("Invalid Email address")
        user=self.model(email=self.normalize_email(email),**exta_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        user=self.create_user(email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """This is a Custom user  model use email insted of username"""

    email =models.EmailField(max_length=255,unique=True)
    name =models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'
