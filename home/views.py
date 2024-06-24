from .models import Profile
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
  return render(req, 'home.html')

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
  
def leaderboard(req):
  users = User.objects.all().order_by('-profile__chips')
  return render(req, 'leaderboard.html',{
    "users": users
  })