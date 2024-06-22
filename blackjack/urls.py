from django.urls import path
from . import views

urlpatterns = [
    path('', views.play, name='blackjack'),
    path('play/', views.play_game, name='play'),
]