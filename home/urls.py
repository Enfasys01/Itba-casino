from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("signup/", views.signup, name="signup"),
  path("signin/", views.signin, name="signin"),
  path("lobby/", views.lobby, name="lobby"),
  path("profile/", views.profile, name="profile"),
  path("signout/", views.signout, name="signout"),
  path("buy_chips/", views.buy_chips, name="buy_chips"),
  path("leaderboard/<str:order_by>", views.leaderboard, name="leaderboard"),
]