"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""
import chess
from chess.engine import PlayResult, Limit
import random
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
import logging
import math
from engines.piece_value import value
from engines.evaluate import evaluate
import yaml


# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
homemade_depth = config["engine"]["homemade_options"]["depth"]


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""


# Bot names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self,
               board: chess.Board,
               time_limit: Limit,
               ponder: bool,  # noqa: ARG002
               draw_offered: bool,
               root_moves: MOVE) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)


class MiniMax(MinimalEngine):
    """Minimax algorithm"""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        logger.info(f"Pre move eval: {evaluate(board=board)}")
        best_move = None #Logger variable
        best_score = 0 #Logger variable
        alpha = -math.inf
        beta = math.inf

        if board.turn:
            max_move_score = -math.inf
            for move in board.legal_moves:
                board.push(move)
                move_score = self.maxi(board=board, alpha=alpha, beta=beta, depth=homemade_depth)
                if move_score > max_move_score:
                    best_move = move
                    max_move_score = move_score
                board.pop()
            best_score = max_move_score
        else:
            min_move_score = math.inf
            for move in board.legal_moves:
                board.push(move)
                move_score = self.mini(board=board, alpha=alpha, beta=beta, depth=homemade_depth)
                if move_score < min_move_score:
                    min_move_score = move_score
                    best_move = move
                board.pop()
            best_score = min_move_score
        
        logger.info(f"Best move: {board.san(best_move)}")
        logger.info(f"Best score: {best_score}")
        board.push(best_move)
        logger.info(f"Post move: {evaluate(board=board)}")
        return PlayResult(move=best_move, ponder=None)
        

    def maxi(self, board: chess.Board, alpha: float, beta: float, depth: int) -> float:
        """Chooses the best score amongs each legal move (Maximum score)"""

        if depth == 0:
            return evaluate(board=board)
        
        best_score = -math.inf
        for move in board.legal_moves:
            board.push(move)
            move_score = self.mini(board=board, alpha=alpha, beta=beta, depth=depth-1)
            board.pop()

            if move_score > best_score:
                # Choose the highest score of the minimums
                best_score = move_score
            
            # Determine a new lower bound -> this node's value >= alpha
            alpha = max(best_score, alpha)

            if beta <= alpha:
                # If we know the minimizer will choose a value less than our current lower bound, we leave this node
                break
        return best_score
    

    def mini(self, board: chess.Board, alpha: float, beta: float, depth: int) -> float:
        """Chooses the best score among each legal move (Minimum score)"""

        if depth == 0:
            return evaluate(board=board)
        
        best_score = math.inf
        for move in board.legal_moves:
            board.push(move)
            move_score = self.maxi(board=board, alpha=alpha, beta=beta, depth=depth-1)
            board.pop()
            
            if move_score < best_score:
                # Choose the lowest score of the maximums
                best_score = move_score
            
            # Determine a new upper bound -> this node's value <= beta
            beta = min(best_score, beta)

            if beta <= alpha:
                # If we know that the maximizer will choose a value greater than our current upper bound, we leave this node
                break
        return best_score
