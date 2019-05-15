from holdem import Table
from holdem import Player

def test_split_current_pot():
    t = Table(small_blind=10, big_blind=20)
    t.add_player(Player(100, t))
    t.add_player(Player(100, t))
    t.add_player(Player(100, t))
    t.add_player(Player(50, t))

    t.new_round()
    print(str(t.next_player()))
    t.next_player().call_check()
    print(str(t.next_player()))
    t.next_player().raise_bet(100)
    print(str(t.next_player()))
    t.next_player().call_check()
    print(str(t.next_player()))
    t.next_player().call_check()
    print(str(t.next_player()))
    t.next_player().call_check()

    print("Pots:")
    for pot in t.pots:
        print(f"{pot.highest_bet}, {pot.stakes}")

    assert len(t.pots) == 2
    assert t.pots[0].highest_bet == 50
    assert t.pots[0].stakes == 200
    assert t.pots[1].highest_bet == 100
    assert t.pots[1].stakes == 150
