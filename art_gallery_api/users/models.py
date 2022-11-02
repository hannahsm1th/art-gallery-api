from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager for creating users and superusers, related to :model:`users.User`
    """

    def create_user(self, email, first_name, last_name, role, password=None, description=None):
        """Creates a new user."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model (
            first_name = first_name,
            last_name = last_name,
            role = role,
            email= self.normalize_email(email),
            description = description
            )
        user.username = email
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role, password, **extra_fields):
        """Creates a new superuser with admin and staff priviliges."""
        user = self.create_user (
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            username = email
            )
        user.username = email
        user.password = make_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Model class for users.
    """
    first_name = models.CharField(max_length=80, blank=False)
    last_name = models.CharField(max_length=80, blank=False)
    email = models.EmailField(blank=False, unique=True)
    STAFF = 'ST'
    MANAGER = 'MA'
    VISITOR = 'VI'
    EDUCATION = 'ED'
    ROLE_CHOICES = [
        (STAFF, 'Staff'),
        (MANAGER,'Manager'),
        (VISITOR,'Visitor'),
        (EDUCATION,'Education'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=VISITOR)
    description = models.CharField(max_length=1000, blank=True, default='')
    created_date = models.DateTimeField(editable=False,auto_now_add=True)
    last_modified = models.DateTimeField(editable=False,auto_now=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'password']

    USERNAME_FIELD = 'email'

    def __str__(self):
        """ The representation that is visible in the admin """
        return self.email