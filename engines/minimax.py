import chess
from chess.engine import PlayResult
import random
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
from piece_value import value

class MiniMax(MinimalEngine):
    """Minimax algorithm"""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        return PlayResult(move=random.choice(list(board.legal_moves)), ponder=None)
    
    def evaluate(self, board: chess.Board) -> float:
        score = 0
        for piece in board.piece_map().values():
            if board.turn:
                score += value(piece.piece_type)
            else:
                score -= value(piece.piece_type)
        return score