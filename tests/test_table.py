from holdem import Table
from holdem import Player


def test_split_current_pot():
    # Table 1
    t1 = Table(small_blind=10, big_blind=20)
    t1.add_player(Player(100, t1))
    t1.add_player(Player(100, t1))
    t1.add_player(Player(100, t1))
    t1.add_player(Player(50, t1))

    t1.new_round()

    t1.next_player().call_check()
    t1.next_player().raise_bet(100)
    t1.next_player().call_check()
    t1.next_player().call_check()
    t1.next_player().call_check()

    assert len(t1.pots) == 2
    assert t1.pots[0].highest_bet == 50
    assert t1.pots[0].stakes == 200
    assert t1.pots[1].highest_bet == 100
    assert t1.pots[1].stakes == 150

    # Table 2
    t2 = Table(small_blind=10, big_blind=20)
    t2.add_player(Player(100, t2))
    t2.add_player(Player(100, t2))
    t2.add_player(Player(50, t2))
    t2.add_player(Player(25, t2))

    t2.new_round()

    t2.next_player().call_check()
    t2.next_player().raise_bet(100)
    t2.next_player().call_check()
    t2.next_player().call_check()
    t2.next_player().call_check()

    assert len(t2.pots) == 3
    assert t2.pots[0].highest_bet == 25
    assert t2.pots[0].stakes == 100
    assert t2.pots[1].highest_bet == 50
    assert t2.pots[1].stakes == 75
    assert t2.pots[2].highest_bet == 100
    assert t2.pots[2].stakes == 100
