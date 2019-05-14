class Player:
    def __init__(self, stakes, table):
        self.stakes = stakes
        self.table = table
        self.bet = 0
        self._has_called = False
        self.hand = None

    def call_check(self):
        if self.has_called():
            raise Exception("This Player has already called")
        highest_bet = self.table.current_pot().highest_bet
        delta = highest_bet - self.bet
        self._bet(delta)
        self._has_called = True
        self.table.set_next_player()

    def raise_bet(self, amount):
        if self.has_called():
            raise Exception("This Player has already called")

        highest_bet = self.table.current_pot().highest_bet
        to_call = highest_bet - self.bet
        delta = amount - to_call

        if delta < 0:
            raise Exception("Raise amount is smaller than to_call amount, consider calling instead")

        # NOT ALL IN
        if amount < self.stakes:
            if delta < self.table.last_bet_raise_delta:
                raise Exception("Delta amount of bet/raise must be at least the last delta amount")
            self.table.last_bet_raise = delta
        # ALL IN
        else:
            pass

        self.table._reset_players_called_var()
        self._bet(amount)
        self._has_called = True
        self.table.set_next_player()

    def fold(self):
        self._has_called = False
        del self.table.active_players[self.table.next_player]
        # next player gets postition of this player, so we dont need to increase the index. 
        # if this player had the last seat, the first player becomes next
        self.table.next_player %= len(self.table.active_players)

    def _bet(self, amount):
        if amount > self.stakes:
            raise Exception("Can't bet more than he has got")
        if amount < 0:
            raise Exception("Can't bet less than 0")
        self.bet += amount
        self.stakes -= amount
        self.table.increase_stakes(amount, self)

    def is_all_in(self):
        return self.stakes == 0
    
    def bet_small_blind(self):
        self._bet(self.table.small_blind)

    def bet_big_blind(self):
        self._bet(self.table.big_blind)
    
    def has_called(self):
        return _has_called or self.is_all_in()
