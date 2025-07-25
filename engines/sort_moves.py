import chess
from engines.piece_value import value
import math

def MVV_LVA(board: chess.Board) -> list[chess.Move]:
    """Most Valuable Victim, Least Valuable Aggressor"""

    def piece_difference(move: chess.Move) -> float:
        """Key function for sorting"""

        if not board.is_capture(move):
            # Non capturing moves always go after capturing moves
            return -math.inf
        if board.is_en_passant(move):
            # en passant is a pawn for a pawn
            return 0.
        
        aggressor_value = value(board.piece_at(move.from_square).piece_type)
        victim_value = value(board.piece_at(move.to_square).piece_type)

        return victim_value - aggressor_value
    
    sorted_list = list(board.legal_moves)
    sorted_list.sort(key=piece_difference, reverse=True)
    return sorted_list


