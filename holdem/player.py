class Player:
    def __init__(self, capital, table):
        self.capital = capital
        self.table = table
        self.bet = 0
        self.has_called = False
        self.cards = None

    def raise_bet(self, amount):
        to_call = self.table.highest_bet - self.bet
        if amount + to_call > self.capital:
            raise Exception("Cant bet more than he has got")
        if amount < self.table.last_raise:
            raise Exception("Must bet/raise at least the last raise amount")
        to_bet = to_call + amount
        self.capital -= to_bet
        self.table.pot += to_bet
        self.bet += to_bet
        self.table.highest_bet = self.bet
        self.table.last_raise = amount
        self.has_called = True

    def call(self):
        highest_bet = self.table.highest_bet
        to_call = highest_bet - self.bet
        if to_call < self.capital:
            self.bet = highest_bet
            self.capital -= to_call
        else:
            self.bet += self.capital
            self.capital = 0
        self.has_called = True

    def check(self):
        if self.bet != self.table.highest_bet:
            raise Exception("Can only check when the players bet is as high as the highest bet in this round")
        self.has_called = True

    def fold(self):
        self.table.players_in_round.remove(self)

    def is_all_in(self):
        return self.capital == 0

    def bet_small_blind(self):
        small_blind = self.table.small_blind
        if self.capital >= small_blind:
            self.capital -= small_blind
            self.bet = small_blind
            self.table.pot += small_blind
        else:
            self.bet = self.capital
            self.table.pot += self.capital
            self.capital = 0
        self.has_called = False

    def bet_big_blind(self):
        big_blind = self.table.big_blind
        if self.capital >= big_blind:
            self.capital -= big_blind
            self.bet = big_blind
            self.table.pot += big_blind
        else:
            self.bet = self.capital
            self.table.pot += self.capital
            self.capital = 0
        self.has_called = False
