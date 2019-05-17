from enum import Enum


class Action:
    def __init__(self, action, amount=-1):
        self.type = action
        self.amount = amount


class Actions(Enum):
    CALL_CHECK = 0
    RAISE_BET = 1
    FOLD = 2
