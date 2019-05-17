from gym.envs.registration import register

register(
    id='holdem_ai_gym-v0',
    entry_point='gym_holdem.envs:HoldemEnv',
)
