from django.shortcuts import render, redirect
from .poker import Game
def play_game(req):
  game = Game(req.user)
  req.session['game'] = game.serialize()
  return redirect('play_poker')

def play(req):
  # print('play',req.session.get('game'))
  game = Game.deserialize(req.session.get('game'), req.user)
  
  winner = None

  if game.state == 'preflop': game.bet = game.blind
  
  if req.method == "POST":
    action = req.POST.get('action')
    if action == 'fold':
      print('player folded')
      game.fold()
    elif action == 'raise':
      print('player raised', req.POST.get('raise'))
      game.raise_(int(req.POST.get('raise')))
    elif action == 'call':
      print('player called', game.bet)
      game.call()
    elif action == 'check':
      print('player checked')
      game.check()
    elif action == 'next_round':
      game.new_round()
      
    if game.state == 'end': winner = game.get_round_winner()
    
    req.session['game'] = game.serialize()
    
    
  

  context = {
    'player': {'chips': game.player.chips, 'hand': game.player.hand.cards, 'bet': game.player.current_bet, 'score': game.get_player_score()},
    'bot': {'chips': game.bot.chips, 'hand': game.bot.hand.cards, 'bet': game.bot.current_bet, 'score': game.get_bot_score()},
    'pot': game.pot,
    'cards': game.cards,
    'blind': game.blind,
    'state': game.state,
    'game_bet': game.bet,
    'winner': winner,
    'dealer': game.dealer
  }
  
  # print('context',context)

  return render(req, 'poker.html',context)