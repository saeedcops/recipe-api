from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **exta_fields):
        """This method is to create user"""
        if not email:
            raise ValueError("Invalid Email address")
        user = self.model(email = self.normalize_email(email), **exta_fields)
        user.set_password(password)

        user.save(using = self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """This is a Custom user  model use email insted of username"""

    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Create Tag model to be used in recipe"""
    name = models.CharField(max_length = 255)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Create Ingredient model to be used in recipe"""
    name = models.CharField(max_length = 255)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Create Recipe model"""
    
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE
    )
    title = models.CharField(max_length = 255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    link = models.CharField(max_length = 255, blank = True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title