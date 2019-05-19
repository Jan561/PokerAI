from gym_holdem.holdem import Table
from gym_holdem.holdem import Player
from gym_holdem.holdem import BetRound


def test_split_pot():
    # Table 1
    t1 = Table(small_blind=10, big_blind=20)
    t1.add_player(Player(100, t1))
    t1.add_player(Player(100, t1))
    t1.add_player(Player(100, t1))
    t1.add_player(Player(50, t1))

    t1.new_round()

    t1.next_player.call_check()
    t1.next_player.raise_bet(100)
    t1.next_player.call_check()
    t1.next_player.call_check()
    t1.next_player.call_check()

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

    t2.next_player.call_check()
    t2.next_player.raise_bet(100)
    t2.next_player.call_check()
    t2.next_player.call_check()
    t2.next_player.call_check()

    assert len(t2.pots) == 3
    assert t2.pots[0].highest_bet == 25
    assert t2.pots[0].stakes == 100
    assert t2.pots[1].highest_bet == 50
    assert t2.pots[1].stakes == 75
    assert t2.pots[2].highest_bet == 100
    assert t2.pots[2].stakes == 100


def test_new_bet_round():
    t = Table(small_blind=10, big_blind=20)
    for _ in range(4):
        t.add_player(Player(100, t))
    
    t.new_round()

    assert t.bet_round == BetRound.PREFLOP
    assert t.last_bet_raise_delta == t.big_blind
    assert len(t.board) == 0
    assert t.next_player_idx == t.next_active_seat(t.big_blind_player)
    for p in t.active_players:
        assert not p.has_called

    t.next_player.raise_bet(50)
    t.next_player.call_check()
    t.next_player.call_check()
    t.next_player.call_check()
    
    assert t.all_players_called
    assert t.bet_round == BetRound.PREFLOP

    t.start_next_bet_round()

    assert t.bet_round == BetRound.FLOP
    assert len(t.board) == 3
    assert t.next_player_idx == t.next_active_seat(t.dealer)
    for p in t.active_players:
        assert not p.has_called

    for _ in range(4):
        t.next_player.call_check()
    
    assert t.bet_round == BetRound.FLOP
    assert t.all_players_called

    t.start_next_bet_round()

    assert t.bet_round == BetRound.TURN
    assert len(t.board) == 4
    assert t.next_player_idx == t.next_active_seat(t.dealer)
    for p in t.active_players:
        assert not p.has_called

    t.next_player.raise_bet(20)
    t.next_player.fold()
    t.next_player.call_check()
    t.next_player.call_check()

    assert len(t.active_players) == 3
    assert t.all_players_called
    assert t.bet_round == BetRound.TURN

    t.start_next_bet_round()

    assert t.bet_round == BetRound.RIVER
    assert len(t.board) == 5
    assert t.next_player_idx == t.next_active_seat(t.dealer)
    for p in t.active_players:
        assert not p.has_called

    for _ in range(3):
        t.next_player.call_check()
    
    assert t.all_players_called
    assert t.bet_round == BetRound.RIVER

    t.start_next_bet_round()

    assert t.bet_round == BetRound.SHOWDOWN
    assert len(t.board) == 5

    t.end_round()

    assert t.bet_round == BetRound.GAME_OVER


def test_all_players_have_called():
    t = Table()
    for _ in range(4):
        t.add_player(Player(100, t))
    t.new_round()

    assert not t.all_players_called
    t.next_player.call_check()
    assert not t.all_players_called
    t.next_player.call_check()
    assert not t.all_players_called
    t.next_player.call_check()
    assert not t.all_players_called
    t.next_player.call_check()
    assert t.all_players_called
    t.start_next_bet_round()
    assert not t.all_players_called

def play_game_0():
    t = Table()
    for _ in range(4):
        t.add(Player(100, table=t))
    
    t.new_round()

    @property
    def n():
        return t.next_player

    n.raise_bet(81)
    n.fold()
    n.fold()
    n.fold()

    t.start_next_bet_round()
    t.end_round()
    t.new_round()

    n.raise_bet(80)
    n.fold()
    n.fold()
    n.call_check()
    
    t.start_next_bet_round()
    t.end_round()
    t.new_round()

    n.action_from_amount(n.stakes)
    n.raise_bet(202)
    n.action_from_amount(n.stakes)

    t.start_next_bet_round()
    t.end_round()
    t.new_round()

    n.raise_bet(209)
    n.action_from_amount(n.stakes)

    t.start_next_bet_round()
    t.end_round()

    assert len(t.players) == 1

def play_game_1():
    t = Table()
    for _ in range(4):
        t.add(Player(100, table=t))
    
    t.new_round()

    @property
    def n():
        return t.next_player
    
    n.raise_bet(75)
    n.raise_bet(100)
    n.fold()
    n.call_check()
    n.action_from_amount(n.stakes)

    t.start_next_bet_round()
    t.end_round()
    t.new_round()


