from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from polymorphic.models import PolymorphicModel, PolymorphicManager

from yatracker.hashes import sha256

from .roles import ROLES


class UserManager(PolymorphicManager, BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **required_args):
        if not email or not password:
            raise ValueError("Users must have an email and password")

        user = self.model(email=email, **required_args)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **required_args):
        user = self.create_user(email, password, **required_args)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(PolymorphicModel, AbstractBaseUser):

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=256)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=3, choices=ROLES)

    # Methods and fields for enabling authentication on this model

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        return user

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_password(self, raw_password):
        if self.email:
            self.password = sha256(self.email + raw_password)

    def check_password(self, raw_password):
        return self.password == sha256(self.email + raw_password)

    def get_full_name(self):
        return '{0} {1}'.format(self.name, self.surname)

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.get_full_name()


class Instructor(User):
    pass


class Student(User):
    pass


class Admin(User):
    pass
