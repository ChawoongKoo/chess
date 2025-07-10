import chess
from engines.piece_value import value
import math

def evaluate(board: chess.Board) -> float:
    score = 0
    for square, piece in board.piece_map().items():
        if piece.color:
            score += value(piece.piece_type)
        else:
            score -= value(piece.piece_type)

    score += mobility_both_sides(board=board)
    return score

def mobility_both_sides(board: chess.Board) -> float:
    score = 0
    if board.turn:
        score += board.legal_moves.count()
        board.turn = not board.turn
        score -= board.legal_moves.count()
        board.turn = not board.turn
    else:
        score -= board.legal_moves.count()
        board.turn = not board.turn
        score += board.legal_moves.count()
        board.turn = not board.turn

    return score
# def evaluate(board: chess.Board) -> float:
#     score = 0
#     for piece in board.piece_map().values():
#         if piece.color:
#             score += value(piece.piece_type)
#         else:
#             score -= value(piece.piece_type)
#     return score