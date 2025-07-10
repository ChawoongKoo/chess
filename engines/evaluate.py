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

    score += mobility_both_sides(board=board)*.1
    return score

def mobility_both_sides(board: chess.Board) -> float:
    score = 0
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
    
    score = white_mobility - black_mobility
    return score

# def evaluate(board: chess.Board) -> float:
#     score = 0
#     for piece in board.piece_map().values():
#         if piece.color:
#             score += value(piece.piece_type)
#         else:
#             score -= value(piece.piece_type)
#     return score