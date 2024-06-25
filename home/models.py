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
    
class Friend_request(models.Model):
  from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
  to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
  state = models.TextField(default='pending')
  
  def send(from_user, to_user):
    print('sending request',from_user, to_user)
    Friend_request.objects.create(from_user=from_user, to_user=to_user)
    
  def get_user_friends(user):
    friend_requests = list(Friend_request.objects.filter(to_user=user, state='accepted')) + list(Friend_request.objects.filter(from_user=user, state='accepted'))
    friends = []
    
    for friend_request in friend_requests:
      if friend_request.from_user == user:
        friends.append(friend_request.to_user)
      else:
        friends.append(friend_request.from_user)
    
    return friends
    