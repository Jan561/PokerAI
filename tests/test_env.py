import gym
import gym_holdem
import numpy as np

def test_creation():
    try:
        gym.make("poker_ai_gym-v0")
    except:
        assert False


def test_random_moves():
    env = gym.make("poker_ai_gym-v0")
    env.reset()
