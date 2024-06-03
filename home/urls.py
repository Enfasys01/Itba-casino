from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("signup/", views.signup, name="signup"),
  path("signin/", views.signin, name="signin"),
  path("lobby/", views.lobby, name="lobby"),
  path("profile/", views.profile, name="profile"),
  path("signout/", views.signout, name="signout"),
]