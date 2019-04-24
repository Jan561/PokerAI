from holdem.table import Table


class Game:
    def __init__(self, players):
        self.players = players
        self.table = Table(players)

    def new_round(self):
        self.players = list(filter(lambda p: p.capital > 0, self.players))
        self.table.players = self.players
        self.table.reset()
        self.table.small_blind_player += 1
        self.table.small_blind_player %= len(self.players)
        self.table.big_blind_player += 1
        self.table.big_blind_player %= len(self.players)
        self.table.distribute_cards()
