from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin


class Address(models.Model):
    CITY_CHOICES = [
        ('abyek', 'آبیک')
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)    
    neighbourhood = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    alley = models.CharField(max_length=50)
    building = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.city}-{self.neighbourhood}-{self.street}-{self.alley}-{self.building}'        