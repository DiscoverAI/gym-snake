import requests


class SnakeBackend:
    def __init__(self, config):
        self.config = config

    def register_new_game(self):
        games_uri = self.config.get_value('backend') + '/games'
        board_height = int(self.config.get_value("board_height"))
        board_width = int(self.config.get_value("board_width"))
        snake_length = int(self.config.get_value("snake_length"))
        response = requests.post(
            games_uri,
            json={'height': board_height, 'width': board_width, 'snakeLength': snake_length},
            headers={'Accept': 'application/json'}
        )
        return response.json()['gameId']

    def make_move(self, direction, game_id):
        direction_uri = self.config.get_value('backend') + '/games/' + game_id + '/tokens/snake/direction'
        response = requests.put(
            direction_uri,
            json={'direction': direction},
            headers={'Accept': 'application/json'}
        )
        return response.json()

    def get_game_info(self, game_id):
        game_uri = self.config.get_value('backend') + '/games/' + game_id
        response = requests.get(game_uri, headers={'Accept': 'application/json'})
        return response.json()
