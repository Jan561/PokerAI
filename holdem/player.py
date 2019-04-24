class Player:
    def __init__(self, capital, table):
        self.capital = capital
        self.table = table
        self.bet = 0
        self.has_called = False
        self.cards = None

    def raise_bet(self, amount):
        delta_own_bet = amount - self.bet
        delta_highest_bet = amount - self.table.highest_bet
        if delta_own_bet > self.capital:
            raise Exception("Cant bet more than he has got")
        if delta_highest_bet < self.table.last_raise:
            raise Exception("Must bet/raise at least the last raise amount")
        self._bet(delta_own_bet)
        self.table.highest_bet = amount
        self.table.last_raise = delta_highest_bet
        self.table.reset_calls()
        self.has_called = True

    def call(self):
        highest_bet = self.table.highest_bet
        to_call = highest_bet - self.bet
        self._bet(to_call)
        self.has_called = True

    def check(self):
        if self.bet != self.table.highest_bet:
            raise Exception("Can only check when the players bet is as high as the highest bet in this round")
        self.has_called = True

    def fold(self):
        self.table.players.remove(self)

    def is_all_in(self):
        return self.capital == 0

    def bet_small_blind(self):
        small_blind = self.table.small_blind
        self._bet(small_blind)
        self.has_called = False

    def bet_big_blind(self):
        big_blind = self.table.big_blind
        self._bet(big_blind)
        self.has_called = False

    def _bet(self, amount):
        if self.capital >= amount:
            self.capital -= amount
            self.bet += amount
            self.table.pot += amount
        else:
            self.bet += self.capital
            self.table.pot += self.capital
            self.capital = 0

    def reset(self):
        self.bet = 0
        self.has_called = False
        self.cards = None
