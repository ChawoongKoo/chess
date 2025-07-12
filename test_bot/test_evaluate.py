import chess
from engines.evaluate import basic_evaluate, relative_evaluate, mobility_score, piece_score
from homemade import MiniMax
import unittest.mock as mock
import math

def test_starting_board() -> None:
    """Assert both sides are equal at the start of the game"""

    board = chess.Board()
    assert basic_evaluate(board=board) == 0

    assert relative_evaluate(board=board) == 0
    board.turn = not board.turn
    assert relative_evaluate(board=board) == 0


def test_basic_evaluate_checkmate() -> None:
    """Assert that a checkmate returns a maximum/minimum score"""

    # White queen checkmate
    board1 = chess.Board(fen="7k/5Q2/7K/8/8/8/8/8 w - - 0 1")
    board1.push_san("Qh7")
    assert board1.is_checkmate()
    assert basic_evaluate(board1) == math.inf

    # Black queen checkmate
    board2 = chess.Board(fen="7K/5q2/7k/8/8/8/8/8 w - - 0 1")
    board2.turn = chess.BLACK
    board2.push_san("Qh7")
    assert board2.is_checkmate()
    assert basic_evaluate(board2) == -math.inf


def test_relative_evaluate_checkmate() -> None:
    """Assert that a checkmate returns a maximum/minimum score"""

    # White queen checkmate
    board1 = chess.Board(fen="7k/5Q2/7K/8/8/8/8/8 w - - 0 1")
    board1.push_san("Qh7")
    assert board1.is_checkmate()
    assert relative_evaluate(board1) == math.inf

    # Black queen checkmate
    board2 = chess.Board(fen="7K/5q2/7k/8/8/8/8/8 w - - 0 1")
    board2.turn = chess.BLACK
    board2.push_san("Qh7")
    assert board2.is_checkmate()
    assert relative_evaluate(board2) == -math.inf


def test_basic_evaluate_mobility_scoring() -> None:
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

    assert basic_evaluate(low_mobility) < basic_evaluate(high_mobility)

def test_relative_evaluate_mobility_scoring() -> None:
    """Assert that the side with more legal moves -> more mobility has an advantage"""

    # Move a3 vs move e3
    low_mobility = chess.Board()
    low_mobility.push(chess.Move.from_uci("a2a3"))
    high_mobility = chess.Board()
    high_mobility.push(chess.Move.from_uci("e2e3"))

    # Black's turn
    assert relative_evaluate(low_mobility) > relative_evaluate(high_mobility)


def test_relative_evaluate_piece_scoring() -> None:
    """Assert that the side with more pieces has an advantage"""

    # Black is missing their A file rook
    board = chess.Board(fen="1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    assert relative_evaluate(board=board) > 0
    board.turn = chess.BLACK
    assert relative_evaluate(board=board) < 0


def test_basic_evaluate_piece_scoring() -> None:
    """Assert that the side with more pieces has an advantage"""

    # Black is missing their A file rook
    board = chess.Board(fen="1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    white_pieces, black_pieces = piece_score(board=board)

    assert white_pieces > black_pieces
    assert basic_evaluate(board=board) > 0