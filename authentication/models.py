from enum import unique
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
    (1, 'bus_admin'),
    (2, 'bus_terminus_admin'),
    (3, 'passenger'),
    (4, 'superuser'),
)


class CustomAccountManager(BaseUserManager):
    def create_superuser(self,  phone, password, ** other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user( phone ,password,**other_fields)

    def create_user(self,  phone,password,**other_fields):
        if not  phone:
            raise ValueError(_('You must provide a phone number'))
        user = self.model( phone= phone, ** other_fields)
        print(password)
        user.set_password('password')
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    fullname = models.CharField(max_length=150, blank=True)
    phone = models.CharField(unique=True,max_length=13)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=4)

    date_joined = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)
