class Pot:
    def __init__(self, stakes=0, contributors=None, highest_bet=0):
        if contributors is None:
            contributors = {}
        self.contributors = contributors
        self.highest_bet = highest_bet
        self.highest_amount = 0
        self.stakes = stakes

    def increase_stakes(self, amount, player):
        if player.bet < self.highest_bet:
            raise Exception(f"Player can't contribute to pot because his bet is too low: player-bet={str(player)}, pot-bet={self.highest_bet}")
        if player not in self.contributors:
            self.contributors[player] = amount
        else:
            self.contributors[player] += amount   
        self.stakes += amount
        self.highest_bet = player.bet
        if amount > self.highest_amount:
            self.highest_amount = amount
