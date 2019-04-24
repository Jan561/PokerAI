import treys
from treys import Deck


class Table:
    def __init__(self, players, small_blind=25, big_blind=50):
        # Players who are still in the round
        self.players = players
        self.pot = 0
        self.highest_bet = 0
        self.last_raise = 0
        self.deck = treys.Deck()
        self.small_blind_player = 0
        self.big_blind_player = 1
        self.small_blind = small_blind
        self.big_blind = big_blind

    def reset(self):
        self.deck = Deck()
        self.pot = 0
        self.highest_bet = self.big_blind
        self.last_raise = self.big_blind
        for player in self.players:
            player.reset()

    def distribute_cards(self):
        for player in self.players:
            player.cards = self.deck.draw(2)

    def reset_calls(self):
        for player in self.players:
            player.has_called = False
