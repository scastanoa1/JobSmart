from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class CustomUserManager(UserManager):
    def create_user(self, mail, password=None, **other_fields):
        if not mail:
            raise ValueError("No has brindado un Email válido")
        mail = self.normalize_email(mail)
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        
        user = self.model(mail=mail, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")
        
        return self.create_user(mail, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    firstName = models.CharField(max_length=40)
    secondName = models.CharField(max_length=40, blank=True)
    lastName = models.CharField(max_length=40)
    mail = models.EmailField(unique=True)
    birth = models.DateField()
    is_staff = models.BooleanField(default=False)        # Agregar este campo
    is_active = models.BooleanField(default=True)        # Agregar este campo para activar el usuario
    is_superuser = models.BooleanField(default=False)    # Agregar este campo

    objects = CustomUserManager()

    USERNAME_FIELD = "mail"
    REQUIRED_FIELDS = ["firstName", "lastName", "birth"]
