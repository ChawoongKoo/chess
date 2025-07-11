import chess
from engines.evaluate import evaluate, mobility_score, piece_score
from homemade import MiniMax
import unittest.mock as mock

def test_starting_board() -> None:
    """Assert both sides are equal at the start of the game"""
    
    board = chess.Board()
    assert evaluate(board=board) == 0

def test_mobility_scoring() -> None:
    """Assert that the side with more legal moves -> more mobility has an advantage"""

    # Move a3 vs move e3
    low_mobility = chess.Board()
    low_mobility.push(chess.Move.from_uci("a2a3"))
    high_mobility = chess.Board()
    high_mobility.push(chess.Move.from_uci("e2e3"))


    low_white, low_black = mobility_score(low_mobility)
    high_white, high_black = mobility_score(high_mobility)
    
    assert low_white < high_white
    assert low_black == high_black


    assert evaluate(low_mobility) < evaluate(high_mobility)

def test_piece_scoring() -> None:
    """Assert that the side with more pieces has an advantage"""

    # Black is missing their A file rook
    board = chess.Board(fen="1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    white_pieces, black_pieces = piece_score(board=board)

    assert white_pieces > black_pieces
    assert evaluate(board=board) > 0