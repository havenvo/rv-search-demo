from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def avatar_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile/avatars', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user to support email instead of user name"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class PetType(models.Model):
    display_name = models.CharField(max_length=120)
    short_code = models.CharField(max_length=20)
    icon_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.display_name


class Country(models.Model):
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ["name", "iso_code"]


class StateProvince(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=60, blank=False)
    country = models.ForeignKey(Country, to_field='iso_code', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(models.Model):
    address_line1 = models.CharField('Address Line 1', max_length=40)
    address_line2 = models.CharField('Address Line 2', max_length=40, blank=True)
    postal_code = models.CharField('Postal Code', max_length=10)
    city = models.CharField(max_length=40, blank=False)
    state_province = models.CharField('State/Province', max_length=40, blank=True)
    country = models.ForeignKey(Country, blank=False, on_delete=models.CASCADE)
    longitude = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5)
    latitude = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5)

    def __str__(self):
        return '%s, %s, %s, %s' % (self.address_line1, self.city, self.state_province, str(self.country))


class ServiceType(models.Model):
    display_name = models.CharField(max_length=120)
    short_code = models.CharField(max_length=20)

    def __str__(self):
        return self.display_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    reviews_count = models.IntegerField(null=True, blank=True, default=0)
    rating_average = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, default=0)
    avatar = models.ImageField(null=True, upload_to=avatar_image_file_path)
    address = models.OneToOneField(Address, blank=True, on_delete=models.CASCADE)
    pet_types = models.ManyToManyField(PetType, blank=True, related_name='profiles')
    pet_num = models.SmallIntegerField(null=True, default=1)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return '[%s %s] %s' % (self.first_name, self.last_name, self.title)


class ServiceRate(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='service_rates')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='service_rates')
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ['service_type', 'profile']

    def __str__(self):
        return '%s, %s, %s' % (self.profile, self.service_type, self.price)
