import random
from home.models import Profile

class Card:
  SUITS = ["Spades", "Hearts", "Clubs", "Diamonds"]
  RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
  VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
  COLORS = {"Spades":"black", "Hearts":"red", "Clubs":"black", "Diamonds":"red"}
  SYMBOLS = {"Spades":"♠", "Hearts":"♥", "Clubs":"♣", "Diamonds":"♦"}
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__(self):
    return f"{self.rank} of {self.suit}"
  
  def display(self):
    return f'<div class="card {self.COLORS[self.suit]}"><span>{self.rank}</span><span>{self.SYMBOLS[self.suit]}</span></div>'
class Deck:
  def __init__(self):
    self.cards = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        self.cards.append(Card(rank, suit))

  def shuffle(self):
    random.shuffle(self.cards)

  def deal(self, cheat=''):
    if cheat:
      return Card(cheat, 'Hearts')
    else:
      return self.cards.pop()
  
class Hand:
  def __init__(self):
    self.cards = []

  def add_card(self, card):
    self.cards.append(card)

  def get_value(self):
    value = 0
    for card in self.cards:
      value += Card.VALUES[card.rank]
    for card in self.cards:
      if value > 21 and card.rank == 'A':
        value -= 10
    return value
      
class Player():
  def __init__(self, profile):
    self.profile = profile
    self.current_bet = 0
    
  def place_bet(self, amount):
    if self.profile.chips >= amount:
      self.profile.chips -= amount
      self.current_bet = amount
      self.save()
  
  def win_bet(self):
    self.profile.chips += 2 * self.current_bet
    self.current_bet = 0
    
  def lose_bet(self):
    self.current_bet = 0
    
  def push_bet(self):
    self.profile.chips += self.current_bet
    self.current_bet = 0
    
  def save(self):
    self.profile.save()
    
class Game:
  def __init__(self, user):
    self.deck = Deck()
    self.deck.shuffle()
    self.player = Player(user.profile)
    self.player_hand = Hand()
    self.player_hand.add_card(self.deck.deal(cheat='A'))
    self.player_hand.add_card(self.deck.deal(cheat='J'))
    self.dealer_hand = Hand()
    self.dealer_hand.add_card(self.deck.deal())
    self.dealer_hand.add_card(self.deck.deal())
    self.game_over = False
    self.state = 'start'
    
  def place_bet(self, amount):
    self.player.place_bet(amount)
  
  def hit(self):
    if self.game_over == False:
      self.player_hand.add_card(self.deck.deal())
      if self.player_hand.get_value() > 21:
        self.game_over = True
        self.get_result()
        self.player.save()

  def stand(self):
    if self.game_over == False:
      while self.dealer_hand.get_value() < 17:
        self.dealer_hand.add_card(self.deck.deal())
      self.game_over = True
      self.state = 'dealer'
      self.get_result()
      self.player.save()

      
  def get_result(self):
    if self.player_hand.get_value() > 21:
      self.player.lose_bet()
      return 'lose'
    elif self.dealer_hand.get_value() > 21:
      self.player.win_bet()
      return 'win'
    elif self.player_hand.get_value() < self.dealer_hand.get_value():
      self.player.lose_bet()
      return 'lose'
    elif self.player_hand.get_value() > self.dealer_hand.get_value():
      self.player.win_bet()
      return 'win'
    else:
      self.player.push_bet()
      return 'draw'
    
  def is_game_over(self):
    return self.game_over
    
  def serialize(self):
    return {
      'player_hand': [(card.rank, card.suit) for card in self.player_hand.cards] if self.player_hand else [],
      'dealer_hand': [(card.rank, card.suit) for card in self.dealer_hand.cards] if self.dealer_hand else [],
      'player_value': self.player_hand.get_value() if self.player_hand else 0,
      'dealer_value': self.dealer_hand.get_value() if self.dealer_hand else 0,
      'game_over': self.game_over,
      'chips':self.player.profile.chips,
      'current_bet': self.player.current_bet,
      'state': self.state
    }

  @staticmethod
  def deserialize(data, user):
    game = Game(user)
    game.player_hand.cards = [Card(rank, suit) for rank, suit in data.get('player_hand', [])]
    game.dealer_hand.cards = [Card(rank, suit) for rank, suit in data.get('dealer_hand', [])]
    game.player_hand.value = data.get('player_value', 0)
    game.dealer_hand.value = data.get('dealer_value', 0)
    game.game_over = data.get('game_over', False)
    game.player.profile.chips = data.get('chips', 500)
    game.player.current_bet = data.get('current_bet', 0)
    game.state = data.get('state', 'player')
    return game