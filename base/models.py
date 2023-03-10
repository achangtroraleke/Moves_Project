from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique =True, null=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']




    
    
class Venue(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    address = models.CharField(max_length=500)


    def __str__(self):
        return self.name

class Poll(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    venues = models.ManyToManyField(
        Venue, related_name='venues', blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True
    )
    area = models.CharField(max_length=300, null=True)


class Option(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    user_votes = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=1)
    
    def __str__(self):
        return self.venue.name    

