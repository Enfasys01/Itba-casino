from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

def home(req):
  return render(req, 'home.html')

def signup(req):
  print(req.POST)
  if req.method == 'POST':
    if req.POST['password'] == req.POST['password2']:
      try:
        user = User.objects.create_user(req.POST['username'], req.POST['email'], req.POST['password'])
        user.save()
        login(req, user)
        return redirect('home')
      except IntegrityError:
        print('Username already taken. Choose another username.')
        return render(req, 'signup.html', {'error': 'Username already taken. Choose another username.', 'form': req.POST}, )
    else:
      print('Passwords do not match')
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
  return render(req, 'profile.html')

def signout(req):
  logout(req)
  return render(req, 'home.html')