import random
from pokereval.card import Card as PECard
from pokereval.hand_evaluator import HandEvaluator

class Card:
  SUITS = ["Spades", "Hearts", "Clubs", "Diamonds"]
  RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
  VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
  COLORS = {"Spades":"black", "Hearts":"red", "Clubs":"black", "Diamonds":"red"}
  SYMBOLS = {"Spades":"♠", "Hearts":"♥", "Clubs":"♣", "Diamonds":"♦"}
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__(self):
    return f"{self.rank} of {self.suit}"
  
  def display(self):
    return f'<div class="card {self.COLORS[self.suit]}"><span>{self.rank}</span><span>{self.SYMBOLS[self.suit]}</span></div>'

  def serialize(self):
    def get_suit(suit):
      if suit == 'Spades':
        return 1
      elif suit == 'Hearts':
        return 2
      elif suit == 'Diamonds':
        return 3
      elif suit == 'Clubs':
        return 4
    return (self.VALUES[self.rank], get_suit(self.suit))

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
    
class Player():
  def __init__(self, chips, profile=None):
    self.chips = chips
    self.current_bet = 0
    self.hand = Hand()
    self.profile = profile
    
  def set_hand(self, cards):
    for card in cards:
      self.hand.add_card(Card(card[0], card[1]))
      
  def bet(self, amount):
    if self.chips >= amount:
      self.chips -= amount
      self.current_bet += amount
      # if self.profile:
        # self.profile.chips -= amount
        # self.profile.save()
        
class Bot(Player):
  def __init__(self, chips):
    super().__init__(chips)
    
  def play(self, score, current_bet=0):
    
    lucky = random.choice([True, False])
    
    def call():
      print('bot called')
      self.bet(current_bet - self.current_bet)
      
    def raise_():
      print('bot raised ', 20)
      self.bet(current_bet + 20)
    
    if current_bet == self.current_bet:
      if lucky:
        # raise_ = int(round(self.chips * 0.2 / 10) * 10)
        # self.bet(raise_)
        # print('bot raised ', raise_)
        raise_()
        return 'raise'
      else:
        print('bot checked')
        return 'check'
    elif score < 15:
      print('bot folded')
      return 'fold'
    elif score < 30:
      if current_bet < self.chips*0.2:
        call()
        return 'call'
      else:
        print('bot folded')
        return 'fold'
    elif score < 60:
      if current_bet < self.chips * 0.5:
        call()
        return 'call'
      else:
        print('bot folded')
        return 'fold'
    elif score < 80:
      if current_bet < self.chips * 0.8:
        call()
        return 'call'
      else:
        print('bot folded')
        return 'fold'
    else:
      raise_()
      # raise_ = int(round(self.chips * 0.5 / 10) * 10)
      # self.bet(raise_)
      # print('bot raised ', raise_)
      return 'raise'
  
class Game():
  def __init__(self, user):
    self.deck = Deck()
    self.deck.shuffle()
    self.player = Player(chips=user.profile.chips, profile = user.profile)
    self.bot = Bot(chips=1000)
    self.deal_players()
    
    
    self.pot = 0
    self.cards = []
    self.blind = 20
    self.bet = 0
    self.state = 'preflop' # preflop, flop, turn, river, end
    self.game_over = False
    self.round = 1
    self.dealer = 'bot'
    self.last_action = 'start'
    
    self.bot.bet(self.blind)
    
  def manage_bot(self, bot_play):
    if bot_play == 'fold':
      self.player.chips += self.pot + self.player.current_bet + self.bot.current_bet
      self.player.current_bet = 0
      self.bot.current_bet = 0
      self.pot = 0
      self.state= 'bot_fold'
    elif bot_play == 'call' or bot_play == 'check':
      self.bet = 0
      self.pot += self.player.current_bet + self.bot.current_bet
      self.player.current_bet = 0
      self.bot.current_bet = 0
      self.deal_table()
    elif bot_play == 'raise':
      self.bet = self.bot.current_bet
    
    self.last_action = 'bot_' + bot_play
    
  def fold(self):
    self.bot.chips += self.pot + self.bot.current_bet + self.player.current_bet
    self.player.current_bet = 0
    self.bot.current_bet = 0
    self.pot = 0
    self.state= 'player_fold'
    
  def call(self):
    self.player.bet(self.bet)
    if(self.last_action != 'start'):
      self.last_action = 'player_call'
      self.manage_bot(self.bot.play(self.get_bot_score(), self.bet))
    else:
      self.last_action = 'player_call'
      self.pot += self.bot.current_bet + self.player.current_bet
      self.player.current_bet = 0
      self.bot.current_bet = 0
      self.bet = 0
      self.deal_table()
    
  def check(self):
    self.last_action = 'player_check'
    self.manage_bot(self.bot.play(self.get_bot_score(), self.bet))

  def raise_(self, amount):
    self.player.bet(amount)
    self.last_action = 'player_raise'
    self.manage_bot(self.bot.play(self.get_bot_score(), amount))

  def deal_players(self):
    self.player.hand = Hand()
    self.bot.hand = Hand()
    for i in range(2):
      self.player.hand.add_card(self.deck.deal())
      self.bot.hand.add_card(self.deck.deal())

  def deal_table(self):
    if self.state == 'preflop':
      for i in range(3):
        self.cards.append(self.deck.deal())
      self.state = 'flop'
    elif self.state == 'flop':
      self.cards.append(self.deck.deal())
      self.state = 'turn'
    elif self.state == 'turn':
      self.cards.append(self.deck.deal())
      self.state = 'river'
    elif self.state == 'river':
      self.end_round()
      self.state = 'end'
      
  def get_round_winner(self):
    player_hand = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.player.hand.cards]
    bot_hand = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.bot.hand.cards]
    board = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.cards]
    
    player_score = HandEvaluator.evaluate_hand(player_hand, board)
    bot_score = HandEvaluator.evaluate_hand(bot_hand, board)
    
    if player_score > bot_score:
      return 'player'
    elif player_score < bot_score:
      return 'bot'
        
  
  def end_round(self):
    result = self.get_round_winner()
    
    if result == 'player':
      self.player.chips += self.pot
    elif result == 'bot':
      self.bot.chips += self.pot
    
    self.pot = 0
      
  def new_round(self):
    self.state = 'preflop'
    self.player.current_bet = 0
    self.bot.current_bet = 0
    self.bet = self.blind
    self.round += 1
    self.cards = []
    self.deal_players()
    
    if self.round%2 == 0:
      self.dealer = 'player'
      self.player.bet(self.blind)
    else:
      self.dealer = 'bot'
      self.bot.bet(self.blind)
    
  def get_bot_score(self):
    hand = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.bot.hand.cards]
    board = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.cards]
    
    return round(HandEvaluator.evaluate_hand(hand, board) * 100)
  
  def get_player_score(self):
    hand = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.player.hand.cards]
    board = [PECard(card.serialize()[0], card.serialize()[1]) for card in self.cards]
    
    return round(HandEvaluator.evaluate_hand(hand, board) * 100)
    
  def serialize(self):
    def serialize_cards(cards):
      return [(card.rank, card.suit) for card in cards]
        
    return{
      'player': {
        'chips': self.player.chips,
        'hand': serialize_cards(self.player.hand.cards),
        'bet': self.player.current_bet
      },
      'bot': {
        'chips': self.bot.chips,
        'hand': serialize_cards(self.bot.hand.cards),
        'bet': self.bot.current_bet
      },
      'pot': self.pot,
      'cards': serialize_cards(self.cards),
      'blind': self.blind,
      'state': self.state,
      'bet': self.bet,
      'round': self.round,
      'dealer': self.dealer
    }  
  
  def deserialize(data, user):
    # print('deserializing', data)
    game = Game(user)
    
    game.player = Player(chips=data.get('player')['chips'], profile = user.profile)
    game.player.set_hand(data.get('player', {}).get('hand', []))
    game.player.current_bet = data.get('player', {}).get('bet', 0)
    game.bot = Bot(chips=data.get('bot')['chips'])
    game.bot.set_hand(data.get('bot', {}).get('hand', []))
    game.bot.current_bet = data.get('bot', {}).get('bet', 0)
    
    game.pot = data.get('pot', 0)
    game.blind = data.get('blind', 20)
    game.state = data.get('state', 'preflop')
    game.bet = data.get('bet', 0)
    game.round = data.get('round', 1)
    game.dealer = data.get('dealer')
    
    game.cards = [Card(rank, suit) for rank, suit in data.get('cards', [])]
    return game