from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uni_res_man.settings import fernet
from django.db.models import Q

class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        total_residents = Resident.objects.filter(room__building=self).count()
        total_rooms = Room.objects.filter(building=self).count()

        if total_residents > total_rooms:
            raise ValidationError("The total number of residents cannot exceed the total number of rooms.")

class Room(models.Model):
    name = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.building}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        total_residents = Resident.objects.filter(room=self).count()
        if total_residents > self.capacity:
            raise ValidationError(f"The room {self.name} has exceeded its capacity.")

class ResidentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class Resident(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = ResidentManager()

    def __str__(self):
        return f"{self.name} - {self.room.name if self.room else 'No Room'}"
    
    def is_admin(self):
        return self.role == 'admin'
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(role='student') | Q(role='admin'),
                name='valid_role_constraint',
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email',
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = fernet.encrypt(self.email.encode()).decode()
        if self.phone:
            self.phone = fernet.encrypt(self.phone.encode()).decode()
        super().save(*args, **kwargs)
    
    def get_decrypted_email(self):
        return fernet.decrypt(self.email.encode()).decode()
    
    def get_decrypted_phone(self):
        return fernet.decrypt(self.phone.encode()).decode()

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - {self.room.name if self.room else 'No Room'}"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
