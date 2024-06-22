from django.urls import path
from . import views

urlpatterns = [
  path('', views.play_game, name='poker'),
  path('play/', views.play, name='play_poker'),
]