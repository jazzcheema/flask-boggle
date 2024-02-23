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
            # TODO: could add comment to test for html
            self.assertEqual(response.status_code, 200)
            self.assertIn("<title>Boggle</title>", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:

            response = client.post('/api/new-game')
            resp_body = response.get_json()
            response.get_data(as_text=True)
            # type(resp_body['game_id']) is type('')
            # type(resp_body['board']) is type([])
            print('response.get_data*********', response.get_data)
            print('response******', response)
            print('response body**************', resp_body)
            print('games************', games)
            ...

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:
            ...
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}
