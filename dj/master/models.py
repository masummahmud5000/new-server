from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, name, username, password=None):
        user = self.model(name=name, username=username)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, username, password=None):
        user = self.create_user(
            name=name,
            username=username,
            password=password
        )
        # user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
    
class Server(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=15)
    username = models.CharField(max_length=30, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    joinDate = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # is_admin = True

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username

