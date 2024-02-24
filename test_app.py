from unittest import TestCase

from app import app, games


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<!-- game_page -->", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:

            response = client.post('/api/new-game')
            resp_body = response.get_json()

            game_id = resp_body["gameId"]
            board = resp_body["board"]
            # FIXME: assert is instance below
            self.assertTrue(type(game_id) is str)
            self.assertTrue(type(board) is list)
            self.assertIn(game_id, games.keys())
            self.assertEqual({'gameId': game_id,
                              'board': board}, resp_body)

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games
            # (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:

            resp = client.post('/api/new-game')
            resp_body = resp.get_json()
            game_id = resp_body['gameId']
            game = games[game_id]
            game.board[0] = ['G', 'B', 'O', 'L', 'K']
            game.board[1] = ['G', 'A', 'O', 'L', 'K']
            game.board[2] = ['G', 'A', 'O', 'H', 'K']
            game.board[3] = ['G', 'A', 'F', 'L', 'K']
            game.board[4] = ['G', 'I', 'R', 'L', 'K']

            resp = client.post(
                '/api/score-word',
                json={
                    'word': 'GIRL',
                    'gameId': game_id
                }
            )
            data = resp.get_json()

            self.assertEqual({'result': 'ok'}, data)

            resp = client.post(
                '/api/score-word',
                json={
                    'word': 'ZEBRA',
                    'gameId': game_id
                }
            )
            data = resp.get_json()

            self.assertEqual({'result': 'not-on-board'}, data)

            resp = client.post(
                '/api/score-word',
                json={
                    'word': 'ZXILO',
                    'gameId': game_id
                }
            )
            data = resp.get_json()

            self.assertEqual({'result': 'not-word'}, data)

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}
