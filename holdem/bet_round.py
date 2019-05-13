from enum import Enum


class BetRound(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4


def next_betround(bet_round):
    new_bet_round = bet_round + 1
    if new_bet_round > 4:
        raise Exception("There is no more betround after Showdown")
    return new_bet_round
