import gym
import numpy as np

from gym.spaces import Box

from gym_holdem.holdem import Table, Player, bet_round_to_str, BetRound

from pokereval_cactus import Card

CALL_CHECK_MOVE = -1
FOLD_MOVE = -2


class HoldemEnv(gym.Env):
    def __init__(self, player_amount=4, small_blind=10, big_blind=20, stakes=100):
        super().__init__()
        self.player_amount = player_amount
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.stakes = stakes
        self.table = None
        self.action_space = Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def step(self, action: np.float32):
        player = self.table.next_player()
        if action < 0 or action > 1:
            raise ValueError()

        self._take_action(action, player)

        if self.table.next_player().has_called():
            self.table.start_next_bet_round()
        
        if self.table.bet_round == BetRound.SHOWDOWN:
            self.table.end_round()

        return self.observation_space, player.stakes, len(self.table.players) == 0, {}

    def reset(self):
        self.table = Table(small_blind=self.small_blind, big_blind=self.big_blind)
        for idx in range(self.player_amount):
            player = Player(self.stakes, self.table)
            self.table.add_player(player)
            player.name = str(idx)

        self.table.new_round()

        return self.observation_space

    def render(self, mode="human", close=False):
        for p in self.table.active_players:
            print(str(p))
        
        print(f"Board: {Card.print_pretty_cards(self.table.board)}")
        print(f"Bet round: {bet_round_to_str(self.table.bet_round)}")

    def get_move_from_action(self, action):
        valid_moves = self._valid_moves
        idx = int(len(valid_moves) * action)
        # For the very rare case that action == 1
        if idx == len(valid_moves):
            idx = len(valid_moves) - 1

        return valid_moves[idx]

    def _take_action(self, action, player):
        move = self.get_move_from_action(action)

        if move == FOLD_MOVE:
            player.fold()
        elif move == CALL_CHECK_MOVE:
            player.call_check()
        elif move > 0:
            # move > 0 indicates raise
            player.raise_bet(move)

    @property
    def _valid_moves(self):
        player = self.table.next_player()
        to_call = self.table.current_pot().highest_bet - player.bet
        min_bet_amount = to_call + self.table.last_bet_raise_delta
        max_bet_amount = player.stakes
        moves = [FOLD_MOVE, CALL_CHECK_MOVE]
        if min_bet_amount <= max_bet_amount:
            possible_bet_amounts = range(min_bet_amount, max_bet_amount + 1)
            moves += possible_bet_amounts
        else:
            if player.stakes > to_call:
                moves.append(player.stakes)

        return np.array(moves)

    @property
    def observation_space(self):
        player = self.table.next_player()

        hand = player.hand
        board = self.table.board
        for _ in range(len(self.table.board), 5):
            board.append(0)
        pot = self.table.pot_value
        player_stakes = player.stakes

        other_players_stakes = []
        for p in self.table.players:
            if p == player:
                continue
            other_players_stakes.append(p.stakes)

        for _ in range(len(self.table.players), self.player_amount):
            other_players_stakes.append(0)

        other_players_active = []
        for p in self.table.players:
            if p == player:
                continue
            active = 1 if p in self.table.active_players else 0
            other_players_active.append(active)

        for _ in range(len(self.table.players), self.player_amount):
            other_players_active.append(-1)
        
        observation = hand + board + [pot, player_stakes] + other_players_stakes + other_players_active
        return np.array(observation)
