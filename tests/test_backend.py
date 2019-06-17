from unittest.mock import patch

from requests.models import Response

from gym_snake.remote import backend
from gym_snake.util import config

mock_register_response = Response()
mock_register_response.json = lambda: {"gameId": "foobar"}

mock_game_info_response = Response()
mock_game_info_response.json = lambda: {"game-info-key": "game-info-value"}

mock_config = config.Config("tests/resources/test-config.json")


@patch('requests.post', return_value=mock_register_response)
def test_register_game(post_mock):
    actual = backend.SnakeBackend(mock_config).register_new_game()
    expected = 'foobar'

    assert expected == actual
    post_mock.assert_called_with(
        'foo backend/games',
        headers={'Accept': 'application/json'},
        json={'height': 1, 'snakeLength': 1, 'width': 1}
    )


@patch('requests.put', return_value=mock_game_info_response)
def test_make_move(put_mock):
    actual = backend.SnakeBackend(mock_config).make_move(direction="up", game_id="foobar")
    expected = {"game-info-key": "game-info-value"}

    assert expected == actual
    put_mock.assert_called_with(
        'foo backend/games/foobar/tokens/snake/direction',
        headers={'Accept': 'application/json'},
        json={"direction": "up"}
    )


@patch('requests.get', return_value=mock_game_info_response)
def test_get_game_info(put_mock):
    actual = backend.SnakeBackend(mock_config).get_game_info(game_id="foobar")
    expected = {"game-info-key": "game-info-value"}

    assert expected == actual
    put_mock.assert_called_with(
        'foo backend/games/foobar',
        headers={'Accept': 'application/json'}
    )
