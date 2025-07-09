import chess
from engines.piece_value import value

def evaluate(board: chess.Board) -> float:
        score = 0
        for piece in board.piece_map().values():
            if piece.color:
                score += value(piece.piece_type)
            else:
                score -= value(piece.piece_type)
        return score