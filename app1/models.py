from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    username = None  
    ADMIN = 1  
    SELLER = 2
    BUYER = 3
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (SELLER, 'Seller'),
        (BUYER, 'Buyer'),
    )
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

  # Roles created here
    mobileno = models.CharField(max_length=10, null=True, blank=True)
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    profilephoto = models.ImageField(upload_to='profilephoto',null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
            return self.email


class ContactMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"