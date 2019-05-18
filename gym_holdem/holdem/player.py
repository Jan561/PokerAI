from gym_holdem.holdem.bet_round import BetRound
from gym_holdem.holdem.poker_rule_violation_exception import PokerRuleViolationException

from pokereval_cactus import Card


class Player:
    def __init__(self, stakes, table=None, name=None):
        self.table = table
        self.name = name
        self.bet = 0
        self.hand = []
        self.stakes = stakes
        self._has_called = False
        self.hand = None

    def reset(self, stakes=0):
        self.bet = 0
        self.hand = []
        self.stakes = stakes
        self._has_called = False
        self.hand = None

    def action_from_amount(self, amount):
        self._check_player_may_act()

        # CHECK || FOLD
        if amount == 0:
            if self.to_call_amount == 0:
                self.call_check()
            else:
                self.fold()

            return

        # CALL || RAISE
        delta = amount - self.to_call_amount

        # IF ALL-IN
        if amount == self.stakes:
            if delta <= 0:
                self.call_check()
            else:
                self.raise_bet(amount)
        else:
            if delta == 0:
                self.call_check()
            elif delta > 0:
                self.raise_bet(amount)
            else:
                raise PokerRuleViolationException(f"Cannot bet less than to call amount: amount=={amount}, to_call=={self.to_call_amount}")


    def call_check(self):
        self._check_player_may_act()

        amount = self.to_call_amount
        # If player must go All-in to call
        if amount > self.stakes:
            amount = self.stakes

        self._bet(amount)
        self._has_called = True
        self.table.set_next_player()

    def raise_bet(self, amount):
        self._check_player_may_act()

        delta = amount - self.to_call_amount

        if delta <= 0:
            raise PokerRuleViolationException("Raise amount is smaller than or equal to to_call amount, consider calling instead")
        
        if amount > self.stakes:
            raise PokerRuleViolationException("Cant bet more than he has got")

        # NOT ALL IN
        if amount < self.stakes:
            if delta < self.table.last_bet_raise_delta:
                raise PokerRuleViolationException(f"Delta amount of bet/raise must be at least the last delta amount, delta== {delta}, last_delta=={self.table.last_bet_raise_delta}")
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
        self._check_player_may_act()

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
    
    @property
    def has_called(self):
        return self._has_called or self.is_all_in()


    @property
    def to_call_amount(self):
        return self.table.current_pot.highest_bet - self.bet

    def _check_player_may_act(self):
        if self.has_called:
            raise PokerRuleViolationException("This Player has already called")
        if self.table.bet_round == BetRound.SHOWDOWN:
            raise PokerRuleViolationException("Cannot bet in showdown")
        if self.table.next_player_idx == None:
            raise PokerRuleViolationException("This betround has already ended")
        if self != self.table.next_player:
            raise PokerRuleViolationException("It's not this players turn")

    def __str__(self):
        if self.name:
            return f"Player {self.name}: bet=={self.bet}, stakes=={self.stakes}, hand=={Card.pretty_print_cards(self.hand)}"
        else:
            return f"Anonymous Player: bet=={self.bet}, stakes=={self.stakes}, hand=={Card.pretty_print_cards(self.hand)}"
