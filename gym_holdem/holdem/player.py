from gym_holdem.holdem.bet_round import BetRound
from gym_holdem.holdem.poker_rule_violation_exception import PokerRuleViolationException

from pokereval_cactus import Card


class Player:
    def __init__(self, stakes, table):
        self.stakes = stakes
        self.table = table
        self.bet = 0
        self._has_called = False
        self.hand = None
        self.name = None # meant to be overwritten

    def call_check(self):
        if self != self.table.next_player():
            raise PokerRuleViolationException("It's not this players turn")
        if self.has_called():
            raise PokerRuleViolationException("This Player has already called")
        if self.table.bet_round == BetRound.SHOWDOWN:
            raise PokerRuleViolationException("Cannot bet in showdown")

        highest_bet = self.table.current_pot().highest_bet
        amount = highest_bet - self.bet
        # If player must go All-in to call
        if amount > self.stakes:
            amount = self.stakes

        self._bet(amount)
        self._has_called = True
        self.table.set_next_player()

    def raise_bet(self, amount):
        if self != self.table.next_player():
            raise PokerRuleViolationException("It's not this players turn")
        if self.has_called():
            raise PokerRuleViolationException("This Player has already called")
        if self.table.bet_round == BetRound.SHOWDOWN:
            raise PokerRuleViolationException("Cannot bet in showdown")

        highest_bet = self.table.current_pot().highest_bet
        to_call = highest_bet - self.bet
        delta = amount - to_call

        if delta < 0:
            raise PokerRuleViolationException("Raise amount is smaller than to_call amount, consider calling instead")
        
        if amount > self.stakes:
            raise PokerRuleViolationException("Cant bet more than he has got")

        # NOT ALL IN
        if amount < self.stakes:
            if delta < self.table.last_bet_raise_delta:
                raise PokerRuleViolationException("Delta amount of bet/raise must be at least the last delta amount")
            self.table.last_bet_raise = delta
        # ALL IN --> self.stakes == amount
        else:
            if delta > self.table.last_bet_raise_delta:
                self.table.last_bet_raise_delta = delta

        self.table.reset_players_called_var()

        self._bet(amount)
        self._has_called = True
        self.table.set_next_player()

    def fold(self):
        if self != self.table.next_player():
            raise PokerRuleViolationException("It's not this players turn")
        if self.has_called():
            raise PokerRuleViolationException("This Player has already called")
        if self.table.bet_round == BetRound.SHOWDOWN:
            raise PokerRuleViolationException("Cannot fold in showdown")

        self._has_called = False
        del self.table.active_players[self.table.next_player_idx]

        self.table.set_next_player(folded=True)

    def _bet(self, amount):
        if amount > self.stakes:
            raise PokerRuleViolationException("Can't bet more than he has got")
        if amount < 0:
            raise PokerRuleViolationException("Can't bet less than 0")

        self.bet += amount
        self.stakes -= amount
        self.table.bet(amount, self)

    def is_all_in(self):
        return self.stakes == 0
    
    def bet_small_blind(self):
        if self.table.small_blind <= self.stakes:
            amount = self.table.small_blind     
        else:
            amount = self.stakes

        self._bet(amount)

    def bet_big_blind(self):
        if self.table.big_blind <= self.stakes:
            amount = self.table.big_blind     
        else:
            amount = self.stakes

        self._bet(amount)
    
    def has_called(self):
        return self._has_called or self.is_all_in()

    def __str__(self):
        if self.name:
            return f"Player {self.name}: bet=={self.bet}, stakes=={self.stakes}, hand=={Card.pretty_print_cards(self.hand)}"
        else:
            return f"Anonymous Player: bet=={self.bet}, stakes=={self.stakes}, hand=={Card.pretty_print_cards(self.hand)}"
