import chess
from chess.engine import PlayResult, Limit
import random
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
import logging

class MiniMax(MinimalEngine):
    """Minimax algorithm"""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        return PlayResult(move=random.choice(list(board.legal_moves)), ponder=None)