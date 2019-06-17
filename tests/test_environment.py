import gym
from unittest.mock import patch
import gym_snake.remote.backend as backend
import numpy as np

game_over_game_state = {
    "game-over": True,
    "board": [[1, 2], [3, 4]],
    "ate-food": False,
    "score": 10
}

game_playing_game_state = {
    "game-over": False,
    "board": [[0, 1], [2, 0]],
    "ate-food": True,
    "score": 10
}


class MockBackend(backend.SnakeBackend):
    def __init__(self, mocked_state):
        super().__init__(self)
        self.mocked_state = mocked_state

    def register_new_game(self):
        return "foobar"

    def make_move(self, direction, game_id):
        return self.mocked_state

    def get_game_info(self, game_id):
        return self.mocked_state


@patch('gym_snake.remote.backend.SnakeBackend', return_value=MockBackend(game_over_game_state))
def test_reset(snake_backend_constructor):
    env = gym.make('snake-v1', config_file="tests/resources/test-config.json")
    initialized_game = env.reset()
    assert "foobar", [0, 1] == initialized_game


@patch('gym_snake.remote.backend.SnakeBackend', return_value=MockBackend(game_over_game_state))
def test_make_step_game_over(snake_backend_constructor):
    environment = gym.make('snake-v1', config_file="tests/resources/test-config.json")
    next_state, reward, done, info = environment.step("up")
    assert reward == -42
    assert np.array_equal(next_state, np.array([[1, 2], [3, 4]], dtype=np.int8))
    assert done
    assert info == {"score": 10}


@patch('gym_snake.remote.backend.SnakeBackend', return_value=MockBackend(game_playing_game_state))
def test_make_step(snake_backend_constructor):
    environment = gym.make('snake-v1', config_file="tests/resources/test-config.json")
    next_state, reward, done, info = environment.step("left")
    assert reward == 42
    assert np.array_equal(next_state, np.array([[0, 1], [2, 0]], dtype=np.int8))
    assert done
    assert info == {"score": 10}
