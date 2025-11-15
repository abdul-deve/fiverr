from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("Invalid Credentials ")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update({
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        })

        if not all([extra_fields.get('is_staff'), extra_fields.get('is_superuser')]):
            raise ValueError("Superuser must have is_staff and is_superuser set to True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLES = (
        ("Buyer","buyer"),
        ("Seller","seller"),
    )
    email = models.EmailField(unique=True,db_index=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    current_role =  models.CharField(max_length=20,choices=ROLES,default="buyer")



    USERNAME_FIELD = 'email'
    objects = UserManager()


    def __str__(self):
        return f"{self.get_username()} {self.email}"
    def is_buyer(self):
        return self.current_role == "buyer"
    def is_seller(self):
        return self.current_role == "seller"
    def verify_email(self,commit=True):
        self.is_email_verified = True
        if commit:
            self.save(update_fields=["is_email_verified"])

    def verify_phone(self,commit=True):
        self.is_phone_verified = True
        self.save()
        if commit:
            self.save(update_fields=["is_phone_verified"])

    def switch_role(self,commit=True):
        buyer , seller = "Buyer","Seller"
        self.current_role = buyer if self.current_role == seller else seller
        if commit:
            self.save(update_fields=["current_role"])

        return self.current_role


