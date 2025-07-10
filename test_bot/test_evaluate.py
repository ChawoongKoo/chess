import chess
from engines.evaluate import evaluate, mobility_both_sides
from homemade import MiniMax
import unittest.mock as mock

def test_starting_board() -> None:
    board = chess.Board()
    assert evaluate(board=board) == 0

def test_mobility_scoring() -> None:
    low_mobility = chess.Board()
    low_mobility.push(chess.Move.from_uci("a2a3"))
    high_mobility = chess.Board()
    high_mobility.push(chess.Move.from_uci("e2e3"))
    assert evaluate(low_mobility) < evaluate(high_mobility)

def test_mobility() -> None:
    low_mobility = chess.Board()
    low_mobility.push(chess.Move.from_uci("a2a3"))
    high_mobility = chess.Board()
    high_mobility.push(chess.Move.from_uci("e2e3"))
    assert mobility_both_sides(low_mobility) < mobility_both_sides(high_mobility)