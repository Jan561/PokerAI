from holdem import Table
from holdem import Player

def test_split_current_pot():
    t = Table()
    t.add_player(Player(500, t))
    t.add_player(Player(500, t))
    t.add_player(Player(500, t))
    t.add_player(Player(400, t))

    t.new_round()
    t.next_player()
