from gym_holdem.holdem import Player
from gym_holdem.holdem import Table
from gym_holdem.holdem import PokerRuleViolationException
from gym_holdem.holdem import BetRound


def test_player_actions():
    t = Table(small_blind=10, big_blind=20)
    for _ in range(4):
        t.add_player(Player(100, t))

    t.new_round()

    assert t.active_players[0].bet == 0
    assert t.active_players[0].stakes == 100
    assert t.active_players[1].bet == 10
    assert t.active_players[1].stakes == 90
    assert t.active_players[2].bet == 20
    assert t.active_players[2].stakes == 80
    assert t.active_players[3].bet == 0
    assert t.active_players[3].stakes == 100

    for p in t.active_players:
        assert not p.has_called()

    for _ in range(4):
        p = t.next_player()
        p.call_check()
        assert p.bet == 20
        assert p.stakes == 80
        assert p.has_called()

    t.start_next_bet_round()

    p = t.next_player()
    p.call_check()
    assert p.bet == 20
    assert p.stakes == 80

    p = t.next_player()
    try:
        p.raise_bet(19)
        assert False
    except PokerRuleViolationException:
        assert p.bet == 20
        assert p.stakes == 80

    p.raise_bet(20)
    assert p.bet == 40
    assert p.stakes == 60
    assert t.current_pot().highest_bet == 40
    assert t.current_pot().highest_amount == 40
    assert p in t.current_pot().contributors
    for other_player in t.active_players:
        if other_player == p:
            continue
        assert not other_player.has_called()

    p = t.next_player()
    p.fold()
    assert not p.has_called()
    assert p.bet == 20
    assert p.stakes == 80
    assert p not in t.active_players

    for _ in range(2):
        t.next_player().call_check()
    
    assert len(t.active_players) == 3
    for p in t.active_players:
        assert p.has_called()
        assert p.bet == 40
        assert p.stakes == 60

    t.start_next_bet_round()

    p = t.next_player()
    p.raise_bet(50)
    p = t.next_player()
    p.raise_bet(60)
    p = t.next_player()
    p.call_check()
    p = t.next_player()
    p.call_check()

    # Player can only perform one action per betround
    try:
        p.fold()
        assert False
    except PokerRuleViolationException:
        pass
    
    for p in t.active_players:
        assert p.is_all_in()

    t.start_next_bet_round()
    assert t.bet_round == BetRound.SHOWDOWN
    assert len(t.board) == 5

    assert len(t.pots) == 1
    assert t.current_pot().highest_bet == 100
    assert t.current_pot().highest_amount == 100
