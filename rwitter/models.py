from math import floor
from numbers import Real
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    follows = models.ManyToManyField("self", related_name='followed_by', symmetrical=False, blank=True)
    profile_picture = models.FileField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

class Rweets(models.Model):
    user = models.ForeignKey(User, related_name='rweets', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (f"{self.user} ({self.created_at: %Y-%m-%d %H:%M}) {self.body[:20]}")