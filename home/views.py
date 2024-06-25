from pytest import console_main
from .models import Friend_request, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

def home(req):
  return render(req, 'home.html')

def signup(req):
  if req.method == 'POST':
    if req.POST['password'] == req.POST['password2']:
      try:
        user = User.objects.create_user(req.POST['username'], req.POST['email'], req.POST['password'])
        user.save()
        login(req, user)
        return redirect('home')
      except IntegrityError:
        return render(req, 'signup.html', {'error': 'Username already taken. Choose another username.', 'form': req.POST}, )
    else:
      return render(req, 'signup.html', {'error': 'Passwords do not match', 'form': req.POST}, )
  else:
    return render(req, 'signup.html')

def signin(req):
  if req.method == 'POST':
    user = User.objects.filter(username=req.POST['username']).first()
    if user is not None and user.check_password(req.POST['password']):
      login(req, user)
      return redirect('home')
    else:
      return render(req, 'signin.html', {'error': 'Invalid username or password', 'form': req.POST}, )
  return render(req, 'signin.html')

def lobby(req):
  return render(req, 'lobby.html')

def friends(req):
  if req.method == 'POST':
    if req.POST.get('unfriend'):
      friend = User.objects.filter(username=req.POST['unfriend']).first()
      friend_request = Friend_request.objects.filter(from_user=req.user,to_user=friend).first()
      if not friend_request: friend_request = Friend_request.objects.filter(from_user=friend,to_user=req.user).first()
      if friend_request: friend_request.delete()
  friends = Friend_request.get_user_friends(req.user)
  return render(req, 'friends.html',{
    'friends': friends,
    'view': 'friends'
  })
  
def friend_requests(req):
  if req.method == 'POST':
    if req.POST.get('accept'):
      from_user = User.objects.filter(username=req.POST['accept']).first()
      friend_request = Friend_request.objects.filter(to_user=req.user,from_user=from_user).first()
      friend_request.state = 'accepted'
      friend_request.save()
    elif req.POST.get('decline'):
      from_user = User.objects.filter(username=req.POST['decline']).first()
      friend_request = Friend_request.objects.filter(to_user=req.user,from_user=from_user).first()
      friend_request.state = 'declined'
      friend_request.save()
  return render(req, 'friends.html',{
    'friends': Friend_request.objects.filter(state='pending',to_user=req.user),
    'view': 'requests'
  })
  
def send_friend_request(req):
  print(req.method)
  if req.method == 'POST':
    if (not Friend_request.objects.filter(from_user=req.user,to_user=User.objects.filter(username=req.POST['to_user']).first()).exists() or not Friend_request.objects.filter(from_user=User.objects.filter(username=req.POST['to_user']).first(),to_user=req.user).exists()) and req.POST['to_user'] != req.user.username:
      to_user = User.objects.filter(username=req.POST['to_user']).first()
      if to_user is not None:
        Friend_request.send(from_user=req.user,to_user=to_user)
  return redirect('friends')

def profile(req):
  all_profiles = Profile.objects.all().order_by('-chips')

  for rank, item in enumerate(list(all_profiles)):
    if item.id == req.user.id:
      break
  
  return render(req, 'profile.html',{
    'rank': rank
  })

def signout(req):
  logout(req)
  return redirect('home')

def buy_chips(req):
  if req.method == 'POST':
    if req.POST['buy'] == '100':
      req.user.profile.chips += 100
    elif req.POST['buy'] == '250':
      req.user.profile.chips += 250
    elif req.POST['buy'] == '500':
      req.user.profile.chips += 500
    elif req.POST['buy'] == '1000':
      req.user.profile.chips += 1000
    req.user.profile.save()
    
  return render(req, 'buy_chips.html',{
    "chips": req.user.profile.chips
  })
  
def leaderboard(req, order_by='chips'):
  print(req.GET.get('list'))
  if req.GET.get('list') == 'friends':
    users = Friend_request.get_user_friends(req.user) + [req.user]
    users.sort(key=lambda x: x.profile.__dict__[order_by], reverse=True)
  else:
    users = User.objects.all().order_by('-profile__'+order_by)
  return render(req, 'leaderboard.html',{
    "users": users,
    "order_by": order_by,
    "list": req.GET.get('list')
  })