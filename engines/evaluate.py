import chess
from engines.piece_value import value
import math


# def evaluate(board: chess.Board) -> float:
#     score = 0

#     """Add up piece values"""
#     for square, piece in board.piece_map().items():
#         if piece.color:
#             score += value(piece.piece_type)
#         else:
#             score -= value(piece.piece_type)

#     """Add up """
#     white_mobility, black_mobility = mobility_both_sides(board=board)
#     score += (white_mobility-black_mobility)*.1

#     return score

def basic_evaluate(board: chess.Board) -> float:
    """Evaluates score of the current board, absolute (white winning -> positive)"""

    if board.is_checkmate():
        return -200. if board.turn else 200.
    score = 0

    white_pieces, black_pieces = piece_score(board=board)
    score += white_pieces - black_pieces

    white_mobility, black_mobility = mobility_score(board=board)
    score += (white_mobility - black_mobility)*.1
    return score


def relative_evaluate(board: chess.Board) -> float:
    """Evaluates score of the current board, relative (White's turn and winning -> positive)"""

    if board.is_checkmate():
        return -200.
    score = 0

    # Add up piece values
    white_pieces, black_pieces = piece_score(board=board)
    score += white_pieces - black_pieces

    # Add up number of legal moves
    white_mobility, black_mobility = mobility_score(board=board)
    score += (white_mobility-black_mobility)*.1

    if not board.turn:
        score *= -1
    return score


def piece_score(board: chess.Board) -> tuple:
    """Returns weighted piece total of each side"""

    white_pieces, black_pieces = 0,0
    for square, piece in board.piece_map().items():
        if piece.color:
            white_pieces += value(piece.piece_type)
        else:
            black_pieces += value(piece.piece_type)
    return white_pieces, black_pieces


def mobility_score(board: chess.Board) -> tuple:
    """Returns total number of legal moves for each side"""

    white_mobility = 0
    black_mobility = 0
    if board.turn:
        white_mobility = board.legal_moves.count()
        board.turn = not board.turn
        black_mobility = board.legal_moves.count()
        board.turn = not board.turn
    else:
        black_mobility = board.legal_moves.count()
        board.turn = not board.turn
        white_mobility = board.legal_moves.count()
        board.turn = not board.turn
    
    return white_mobility, black_mobility