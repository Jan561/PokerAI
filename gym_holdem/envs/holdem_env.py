import gym
import numpy as np

from gym.spaces import Discrete

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
        self.done = True
        # 0 -> FOLD
        # 1 -> CALL || CHECK
        # 2 -> ALL_IN
        # 3..(stakes * player_amount + 2) -> bet_amount + 2
        self.action_space = Discrete(stakes * player_amount + 3)
        self.players = [Player(stakes, str(i)) for i in range(player_amount)]
        self.reset()

    def step(self, action: int):
        player = self.table.next_player
        if action not in self.valid_actions:
            raise ValueError(f"Action {action} is not valid in this context")

        self._take_action(action, player)

        if self.table.all_players_called:
            self.table.start_next_bet_round()
        
        done = False
        if self.table.bet_round == BetRound.SHOWDOWN:
            self.table.end_round()
            if len(self.table.players) >=2:
                self.table.new_round()
            else:
                done = True

        return self.observation_space(player), player.stakes, done, {}

    def reset(self):
        self.table = Table(small_blind=self.small_blind, big_blind=self.big_blind)
        for p in self.players:
            p.reset(stakes=self.stakes)
            p.table = self.table
        self.table.players = self.players[:]

        self.table.new_round()

        return self.observation_space(self.table.next_player)

    def render(self, mode="human", close=False):
        for p in self.table.active_players:
            print(str(p))
        
        print(f"Board: {Card.print_pretty_cards(self.table.board)}")
        print(f"Bet round: {bet_round_to_str(self.table.bet_round)}")

    def _take_action(self, action, player):
        if action == 0:
            player.fold()
        elif action == 1:
            player.call_check()
        elif action == 2:
            player.action_from_amount(player.stakes)
        else:
            player.raise_bet(action - 2)

    @property
    def valid_actions(self):
        player = self.table.next_player
        to_call = player.to_call_amount
        min_bet_amount = to_call + self.table.last_bet_raise_delta
        max_bet_amount = player.stakes
        # 0 -> FOLD
        # 1 -> CALL || CHECK
        actions = [0, 1, 2]
        if min_bet_amount <= max_bet_amount:
            possible_bet_actions = range(min_bet_amount + 2, max_bet_amount + 3)
            actions += possible_bet_actions
        # else:
        #    if player.stakes > to_call:
        #        actions.append(player.stakes)

        return np.array(actions)

    def observation_space(self, player):
        hand = player.hand

        board = self.table.board[:]
        for _ in range(len(self.table.board), 5):
            board.append(0)
        pot = self.table.pot_value

        player_stakes = player.stakes

        other_players_stakes = []
        for p in self.players:
            if p == player:
                continue
            other_players_stakes.append(p.stakes)

        player_active = 1 if player in self.table.active_players else 0

        other_players_active = []
        for p in self.players:
            if p == player:
                continue
            active = 1 if p in self.table.active_players else 0
            other_players_active.append(active)
        
        observation = hand + board + [pot, player_stakes] + other_players_stakes + [player_active] + other_players_active
        return np.array(observation)

    @property
    def table_players(self):
       return self.table.players

    @property
    def next_player(self):
        return self.table.next_player
