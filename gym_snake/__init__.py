from gym.envs.registration import register

register(
    id='snake-v1',
    entry_point='gym_snake.envs:SnakeEnv',
)
