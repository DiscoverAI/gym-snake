import gym

import gym_snake.remote.backend as backend
import gym_snake.util.config as config
from gym import spaces
import numpy as np


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        self.config = config.Config(kwargs.get("config_file", "resources/default-config.json"))
        self.backend = backend.SnakeBackend(self.config)
        self.current_game_id = None
        self.observation_space = spaces.Box(0,
                                            3,
                                            (int(self.config.get_value("board_width")),
                                             int(self.config.get_value("board_height"))))
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        action_to_string = {0: "left", 1: "right", 2: "up", 3: "down"}.get(action, action)
        next_state = self.backend.make_move(action_to_string, self.current_game_id)
        reward = self.get_reward(next_state)
        game_over = next_state["game-over"]
        info = {"score": next_state["score"]}
        return np.array(next_state["board"], dtype=np.int8), reward, game_over, info

    def reset(self):
        self.current_game_id = self.backend.register_new_game()
        game_info = self.backend.get_game_info(self.current_game_id)
        return np.array(game_info["board"], dtype=np.int8)

    def render(self, mode='human'):
        pass  # Here one can log human readable state of the environment

    def close(self):
        pass

    def get_reward(self, game_state):
        if game_state["game-over"]:
            return float(self.config.get_value("game_over_reward"))
        elif game_state["ate-food"]:
            return float(self.config.get_value("ate_food_reward"))
        else:
            return float(self.config.get_value("snake_moved_reward"))
