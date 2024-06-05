from django.shortcuts import render, redirect
from .blackjack import Game

def play_game(req):
  game = Game()
  req.session['game'] = game.serialize()
  return redirect('play')

def play(req):
  game = Game.deserialize(req.session.get('game'))

  if req.method == "POST":
    
    if game.state == 'start':
      game.state = 'player'
    
    action = req.POST.get('action')
    if action == 'hit':
      game.hit()
    elif action == 'stand':
      game.stand()
    elif action == 'bet':
      amount = int(req.POST.get('bet_amount', 0))
      game.place_bet(amount)

    req.session['game'] = game.serialize()
    
  if game.is_game_over():
    game.get_result()

  context = {
    'player_hand': game.player_hand.cards,
    'dealer_hand': game.dealer_hand.cards,
    'player_value': game.player_hand.get_value(),
    'dealer_value': game.dealer_hand.get_value(),
    'is_game_over': game.is_game_over(),
    'state': game.state,
    'chips': game.player.chips,
    'current_bet': game.player.current_bet,
    'result': game.get_result()
  }
  return render(req, 'game.html', context)
