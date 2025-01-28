from django.db import models
from django.utils.timezone import now  # Import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

# Room model
class Room(models.Model):
    image = models.ImageField(upload_to='room_images/')  
    title = models.CharField(max_length=100)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    location = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    description = models.TextField(max_length=500)  

    def __str__(self):
        return self.title


# Booking model
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(default=now)  # Add default value here

    def __str__(self):
        return f"Booking by {self.user.email} for {self.room.title}"


# Review model
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)  # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.room.title}"


# UserManager for custom User model
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2 = None):
        """
        Creates and saves a User with the given email, name, tc, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not tc:
            raise ValueError("Users must agree to the terms and conditions")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        """
        Creates and saves a superuser with the given email, name, tc, and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            tc=tc,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    tc = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
