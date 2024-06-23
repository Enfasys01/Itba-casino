from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
  
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  chips = models.IntegerField(default=1000)
  poker_wins = models.IntegerField(default=0)
  blackjack_wins = models.IntegerField(default=0)

  def __str__(self):
    return f'{self.user.username} Profile'

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(user=instance)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)