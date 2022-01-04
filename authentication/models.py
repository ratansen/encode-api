import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
    (1, 'BUSADMIN'),
    (2, 'BUS TERMINUS ADMIN'),
    (3, 'PASSENGER'),
)

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('username', 'superuser')
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,  ** other_fields)
        user.set_password(password)
        user.save()
        return user



class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=False, default="user")
    fullname = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField(unique=False, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)


    date_joined = models.DateTimeField(default=timezone.now)
    provider = models.CharField(max_length=200, unique=False, default="email")
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)


