import chess
from engines.evaluate import evaluate

def test_starting_board() -> None:
    board = chess.Board()
    assert evaluate(board=board) == 0