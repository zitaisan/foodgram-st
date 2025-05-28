from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """
    Customized user model.
    Registration using email.
    """
    USER = 'user'
    ADMIN = 'admin'
    ROLE_USER = [
        (USER, 'User'),
        (ADMIN, 'Administrator')
    ]
    username = models.CharField('Username', max_length=150, unique=True)
    first_name = models.CharField('First name', max_length=150)
    last_name = models.CharField('Last name', max_length=150)
    email = models.EmailField('Email address', unique=True)
    role = models.CharField(
        max_length=15,
        choices=ROLE_USER,
        default=USER,
        verbose_name='User role'
    )
    password = models.CharField(max_length=150, verbose_name='Password')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',  # уникальное имя
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',  # уникальное имя
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
