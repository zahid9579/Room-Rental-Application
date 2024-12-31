from django.db import models
from django.contrib.auth.models import User  # Use default User model


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


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.title}"


# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField() 

    def __str__(self):
        return f"Review by {self.user.username} for {self.room.title}"
