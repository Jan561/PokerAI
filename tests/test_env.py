import gym
import gym_holdem
import numpy as np

def test_creation():
    try:
        gym.make("poker_ai_gym-v0")
    except:
        assert False


def test_everyone_checks():
    env = gym.make("poker_ai_gym-v0")
    
    env.step(1)
    env.step(1)
    env.step(1)
    env.step(1)

    env.step(0)
    env.step(0)
    env.step(0)
    env.step(0)

    env.step(0)
    env.step(0)
    env.step(0)
    env.step(0)

    env.step(0)
    env.step(0)
    env.step(0)
    env.step(0)

    env.step(0)
    env.step(0)
    env.step(0)
    env.step(0)

def play_game_0():
    env = gym.make("poker_ai_gym-v0")
    env.step(83)
    env.step(0)
    env.step(0)
    env.step(0)
    
    env.step(82)
    env.step(0)
    env.step(0)
    env.step(1)

    env.step(211)
    env.step(2)


def play_game_1():
    env = gym.make("poker_ai_gym-v0")
    env.step(77)
    env.step(102)
    env.step(0)
    env.step(1)
    env.step(2)

def play_game_0_and_1():
    env = gym.make("poker_ai_gym-v0")
    env.reset()
    
    env.step(83)
    env.step(0)
    env.step(0)
    env.step(0)
    
    env.step(82)
    env.step(0)
    env.step(0)
    env.step(1)

    env.step(211)
    env.step(2)

    env.reset()

    env.step(77)
    env.step(102)
    env.step(0)
    env.step(1)
    env.step(2)
