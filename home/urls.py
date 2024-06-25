from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("signup/", views.signup, name="signup"),
  path("signin/", views.signin, name="signin"),
  path("lobby/", views.lobby, name="lobby"),
  path("profile/", views.profile, name="profile"),
  path("friends/", views.friends, name="friends"),
  path("friends/requests", views.friend_requests, name="friend_requests"),
  path("send_friend_request/", views.send_friend_request, name="send_friend_request"),
  path("signout/", views.signout, name="signout"),
  path("buy_chips/", views.buy_chips, name="buy_chips"),
  path("leaderboard/<str:order_by>", views.leaderboard, name="leaderboard"),
]