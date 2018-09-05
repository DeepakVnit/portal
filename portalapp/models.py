# Create your models here.
import jwt

from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Profile(TimestampedModel):
    user = models.OneToOneField(
        'portalapp.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='mystatic/', default="mystatic/None/1.jpg", max_length=255)

    def __str__(self):
        return self.user.username


class Basic(TimestampedModel):
    STATES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadar and Nagar Haveli', 'Dadar and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry'),
    )
    profile = models.OneToOneField(
        'portalapp.Profile', on_delete=models.CASCADE
    )
    dob = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=12, default="XXXXXXX")
    alternate_phone = models.CharField(max_length=12, default="XXXXXXXX")
    city = models.CharField(max_length=50, default="Bengaluru")
    state = models.CharField(max_length=50, choices=STATES, default="Karnataka")
    country = models.CharField(max_length=50, default='India')
    interest = models.CharField(max_length=200, default="Web Development")
    website = models.CharField(max_length=200, default="https://bbc.com/")


class Experience(TimestampedModel):
    profile = models.ForeignKey('portalapp.Profile', on_delete=models.CASCADE)
    designation = models.CharField(max_length=150, default="Software Developer")
    company = models.CharField(max_length=150, default="SAP")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)


class Education(TimestampedModel):
    profile = models.ForeignKey('portalapp.Profile', on_delete=models.CASCADE)
    education_level = models.CharField(max_length=150, default="B.Tech.")
    branch = models.CharField(max_length=150, default="Compuetr Science Engineering")
    institute = models.CharField(max_length=150, default="VNIT Nagpur")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)


class Skill(TimestampedModel):
    profile = models.ForeignKey('portalapp.Profile', on_delete=models.CASCADE)
    skill = models.CharField(max_length=150, default="Java")
    last_used = models.DateField(default=timezone.now)


class Project(TimestampedModel):
    PROJECT_TYPE = (
        ('Self', 'Self'),
        ('Institute', 'Institute'),
    )
    profile = models.ForeignKey('portalapp.Profile', on_delete=models.CASCADE)
    headline = models.CharField(max_length=200, default="Django project")
    description = models.TextField(max_length=300, blank=True)
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(default=timezone.now)
    ptype = models.CharField(max_length=50, choices=PROJECT_TYPE, default="Self")
    extra_info = models.TextField(max_length=100, default="salary 13.3 lpa")
