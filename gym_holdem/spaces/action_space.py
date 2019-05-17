from gym import spaces
import numpy as np
import random


class ActionSpace(spaces.Space):
    def __init__(self, actions):
        self.actions = actions
        super().__init__((), np.int32)

    def sample(self):
        return random.choice(self.actions)

    def contains(self, x):
        if isinstance(x, int) or (
                isinstance(x, (np.generic, np.ndarray)) and
                x.dtype.kind in np.typecodes['AllInteger'] and x.shape == ()
        ):
            return int(x) in self.actions
        else:
            return False

    def __repr__(self):
        min_bet = self.actions[2] if len(self.actions) >= 3 else -1
        max_bet = self.actions[-1] if len(self.actions) >= 3 else -1
        return f"ActionSpace({min_bet}, {max_bet})"

    def __eq__(self, other):
        return isinstance(other, ActionSpace) and self.actions == other.actions
