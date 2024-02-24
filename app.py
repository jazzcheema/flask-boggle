from flask import Flask, request, render_template, jsonify
from uuid import uuid4


from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    # TODO: better name for below.. not a string yet..
    return jsonify({'gameId': game_id, 'board': game.board})


@app.post("/api/score-word")
def score_word():
    """Takes in a Word and ID from game instance and checks if word is valid and
    present on current board--> returns a json string.

   JSON BODY: {
       "word": "ZOO",
       "gameId": "asdasd-asdsdas-...."
    }

    Returns: JSON of {
       "result": "ok"
    }
    """

    word = request.json["word"]
    id = request.json["gameId"]

    if not games[id].is_word_in_word_list(word):
        return jsonify({"result": "not-word"})

    if not games[id].check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})
