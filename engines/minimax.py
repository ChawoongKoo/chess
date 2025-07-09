import chess
from chess.engine import PlayResult
import random
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import HOMEMADE_ARGS_TYPE
from piece_value import value
from evaluate import evaluate
import math

class MiniMax(MinimalEngine):
    """Minimax algorithm"""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        best_move = None
        if board.turn:
            max_move_score = -math.inf
            for move in board.legal_moves:
                board.push(move)
                move_score = self.maxi(board=board, depth=2-1)
                max_move_score = max(move_score, max_move_score)
                best_move = move
                board.pop()
        else:
            min_max_score = math.inf
            for move in board.legal_moves:
                board.push(move)
                move_score = self.mini(board=board, depth=2-1)
                max_move_score = min(move_score, max_move_score)
                best_move = move
                board.pop()
            
        return PlayResult(move=best_move, ponder=None)
    
    # def negamax(self, board: chess.Board, turn: bool, depth: int) -> float:
    #     """Negamax implementation"""

    #     if depth == 0:
    #         return self.evaluate(board=board)
        
    #     if turn:
    #         minimum = -math.inf
    #         for move in board.legal_moves:
    #             board.push(move)
    #             move_score = self.mini(board=board, depth=depth-1)
                
    #             if move_score > minimum:
    #                 minimum = move_score
    #             board.pop()
    #         return minimum
        
    #     else:
    #         maximum = math.inf
    #         for move in board.legal_moves:
    #             board.push(move)
    #             move_score = self.maxi(board=board, depth=depth-1)
                
    #             if move_score < maximum:
    #                 maximum = move_score
    #             board.pop()
    #         return maximum
        

    def maxi(self, board: chess.Board, depth: int) -> float:
        """Maximizes the minimum score of each possible move"""

        if depth == 0:
            return evaluate(board=board)
        
        minimum = -math.inf
        for move in board.legal_moves:
            board.push(move)
            move_score = self.mini(board=board, depth=depth-1)
            
            if move_score > minimum:
                minimum = move_score
            board.pop()
        return minimum
    

    def mini(self, board: chess.Board, depth: int) -> float:
        """Minimizes the maximum score of each possible move"""

        if depth == 0:
            return evaluate(board=board)
        
        maximum = math.inf
        for move in board.legal_moves:
            board.push(move)
            move_score = self.maxi(board=board, depth=depth-1)
            
            if move_score < maximum:
                maximum = move_score
            board.pop()
        return maximum