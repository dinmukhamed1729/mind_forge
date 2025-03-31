from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'user'
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')],
        default='student'
    )
    rating = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )
