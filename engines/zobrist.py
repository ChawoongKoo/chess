import chess
import random

def init_zobrist() -> dict:
    """Returns a dict of hash numbers for each square-piece-color and castling rights, en passant"""
    bit_length = 64

    zobrist_numbers = {}
    # Zobrist init hash for each piece/square
    for square in chess.SQUARES:
        for piece in chess.PIECE_TYPES:
            for color in chess.COLORS:
                zobrist_numbers[(square,piece,color)] = random.getrandbits(bit_length)

    # Castling rights hash
    board = chess.Board() # Initizalize a starting position
    # Each rook has a hash if it can castle
    zobrist_numbers[board.castling_rights & chess.BB_A1] = random.getrandbits(bit_length)
    zobrist_numbers[board.castling_rights & chess.BB_A8] = random.getrandbits(bit_length)
    zobrist_numbers[board.castling_rights & chess.BB_H1] = random.getrandbits(bit_length)
    zobrist_numbers[board.castling_rights & chess.BB_H8] = random.getrandbits(bit_length)

    # each file has a hash if it is enpassant
    for file in chess.FILE_NAMES:
        zobrist_numbers[file] = random.getrandbits(bit_length)

    zobrist_numbers[chess.BLACK] = random.getrandbits(bit_length)

    return zobrist_numbers
    
    
def starting_zobrist_hash(zobrist_numbers: dict) -> int:
    board = chess.Board()
    z_hash = 0
    for square, piece in board.piece_map().items():
        z_hash ^= zobrist_numbers[(square, piece.piece_type, piece.color)]
    
    z_hash ^= zobrist_numbers[board.castling_rights & chess.BB_A1]
    z_hash ^= zobrist_numbers[board.castling_rights & chess.BB_A8]
    z_hash ^= zobrist_numbers[board.castling_rights & chess.BB_H1]
    z_hash ^= zobrist_numbers[board.castling_rights & chess.BB_H8]

    return z_hash

board = chess.Board()
print(format(board.castling_rights, "064b"))
print(board.ep_square)
zobrist_numbers = init_zobrist()
print(format(starting_zobrist_hash(zobrist_numbers), '064b'))