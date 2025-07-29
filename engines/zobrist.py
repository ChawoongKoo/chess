import chess
import random

def init_zobrist() -> list[int]:
    bit_length = 64

    zobrist_numbers = []
    for i in range(781):
        zobrist_numbers.append(random.getrandbits(bit_length))
    
    return zobrist_numbers
    
    
def zobrist_hash(board: chess.Board) -> int:
    z_hash = 0
    for square, piece in board.piece_map():
        