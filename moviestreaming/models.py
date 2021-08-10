from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User, BaseUserManager

# Create your models here.
from django.forms import ModelForm, forms, PasswordInput, EmailInput


class UserAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, first_name, last_name, password):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Please set email'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

    def create_normal_user(self, email, first_name, last_name, password):
        """

        :param email:
        :param first_name:
        :param last_name:
        :param password:
        :return:
        """
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.save()


class UserC(AbstractBaseUser):
    """
    Class(model) for saving User detail

    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=20, unique=True)
    password = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserAccountManager()

    class Meta:
        """

        """
        app_label = 'moviestreaming'

    def __str__(self):
        """

        :return:
        """
        return "{0} , {1} ".format(self.first_name, self.last_name, self.password, self.email)


class Movie(models.Model):
    """
    Class for adding Movie
    """
    title = models.CharField(max_length=35)
    year = models.IntegerField(null=True)
    movie_url = models.URLField(null=True)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        """

        """
        app_label = 'moviestreaming'


class Review(models.Model):
    """
    Class for reviews including comments and rating of Movie. This class has Movie ID and User ID
    as a foreign keys

    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(UserC, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        """

        """
        app_label = 'moviestreaming'
        unique_together = (("user", "movie"),)

    def __str__(self):
        """

        :return:
        """
        return "{0} , {1} ".format(self.movie, self.user, self.rating, self.created_at)
