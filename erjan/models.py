from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username = username,
            email = email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username = username,
            email = email,
            password = password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user




class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    otp = models.CharField(max_length=6, null=True, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
