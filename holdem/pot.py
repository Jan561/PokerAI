class Pot:
    def __init__(self, stakes=0, contributors=None, highest_bet=0):
        if contributors is None:
            contributors = []
        self.contributors = contributors
        self.highest_bet = highest_bet
        self.stakes = stakes

    def increase_stakes(self, amount, player):
        if player.bet < self.highest_bet:
            raise Exception("Player can't contribute to pot because his bet is too low")
        self.contributors.append(player)
        self.stakes += amount
        self.highest_bet = player.bet
