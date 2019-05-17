class Pot:
    def __init__(self, stakes=0, contributors=None, highest_bet=0):
        if contributors is None:
            contributors = {}
        self.contributors = contributors
        self.highest_bet = highest_bet
        self.stakes = stakes

    def increase_stakes(self, amount, player, auto_set_highest_bet=True):
        if player.bet < self.highest_bet:
            raise Exception(f"Player can't contribute to pot because his bet is too low: player-bet=={str(player)}, "
                            f"pot-bet=={self.highest_bet}")

        if player not in self.contributors:
            self.contributors[player] = amount
        else:
            self.contributors[player] += amount

        self.stakes += amount
        if auto_set_highest_bet:
            self.highest_bet = player.bet

    @property
    def highest_amount(self):
        if len(self.contributors) == 0:
            return 0
        max_key = max(self.contributors, key=self.contributors.get)
        return self.contributors[max_key]
