import chess
import random

random.seed(42)

class Zobrist():
    def __init__(self):
        # Starting hash is the hash of the starting board
        self.zobrist_numbers = self._init_zobrist()
        self.curr_hash = self._starting_zobrist_hash(self.zobrist_numbers)

    def update(self, board: chess.Board, move: chess.Move) -> None:
        if board.is_kingside_castling(move):
            if board.turn:
                # update king position, kingside rook position, whiteside castling rights
                self.curr_hash ^= self.zobrist_numbers[(chess.E1, chess.KING, chess.WHITE)]
                self.curr_hash ^= self.zobrist_numbers[(chess.G1, chess.KING, chess.WHITE)]

                self.curr_hash ^= self.zobrist_numbers[(chess.H1, chess.ROOK, chess.WHITE)]
                self.curr_hash ^= self.zobrist_numbers[(chess.F1, chess.ROOK, chess.WHITE)]

                self.curr_hash ^= self.zobrist_numbers["whitekingside"]
                self.curr_hash ^= self.zobrist_numbers["whitequeenside"]
            else:
                # update king position, kingside rook position, blackside castling rights
                self.curr_hash ^= self.zobrist_numbers[(chess.E8, chess.KING, chess.BLACK)]
                self.curr_hash ^= self.zobrist_numbers[(chess.G8, chess.KING, chess.BLACK)]

                self.curr_hash ^= self.zobrist_numbers[(chess.H8, chess.ROOK, chess.BLACK)]
                self.curr_hash ^= self.zobrist_numbers[(chess.F8, chess.ROOK, chess.BLACK)]

                self.curr_hash ^= self.zobrist_numbers["blackkingside"]
                self.curr_hash ^= self.zobrist_numbers["blackqueenside"]
        elif board.is_queenside_castling(move):
            if board.turn:
                # update king position, queenside rook position, whiteside castling rights
                self.curr_hash ^= self.zobrist_numbers[(chess.E1, chess.KING, chess.WHITE)]
                self.curr_hash ^= self.zobrist_numbers[(chess.C1, chess.KING, chess.WHITE)]

                self.curr_hash ^= self.zobrist_numbers[(chess.A1, chess.ROOK, chess.WHITE)]
                self.curr_hash ^= self.zobrist_numbers[(chess.D1, chess.ROOK, chess.WHITE)]

                self.curr_hash ^= self.zobrist_numbers["whitekingside"]
                self.curr_hash ^= self.zobrist_numbers["whitequeenside"]
            else:
                # update king position, queenside rook position, blackside castling rights
                self.curr_hash ^= self.zobrist_numbers[(chess.E8, chess.KING, chess.BLACK)]
                self.curr_hash ^= self.zobrist_numbers[(chess.C8, chess.KING, chess.BLACK)]

                self.curr_hash ^= self.zobrist_numbers[(chess.A8, chess.ROOK, chess.BLACK)]
                self.curr_hash ^= self.zobrist_numbers[(chess.D8, chess.ROOK, chess.BLACK)]

                self.curr_hash ^= self.zobrist_numbers["blackkingside"]
                self.curr_hash ^= self.zobrist_numbers["blackqueenside"]
        
        else:
            # update moving piece position
            self.curr_hash ^= self.zobrist_numbers[(move.from_square, board.piece_at(move.from_square), board.color_at(move.from_square))]

            if move.promotion:
                self.curr_hash ^= self.zobrist_numbers[(move.to_square, move.promotion, board.color_at(move.from_square))]
            else:
                self.curr_hash ^= self.zobrist_numbers[(move.to_square, board.piece_at(move.from_square), board.color_at(move.from_square))]

            if board.is_capture(move):
                # update taken piece
                self.curr_hash ^= self.zobrist_numbers[(move.to_square, board.piece_at(move.to_square), board.color_at(move.to_square))]
            
            if board.piece_at(move.from_square) == chess.KING and board.has_castling_rights(board.color_at(move.from_square)):
                # If the king is the moving piece, assuming that this move is NOT a castling move and the color may castle, 
                # get rid of that color's castling rights
                if board.color_at(move.from_square):
                    self.curr_hash ^= self.zobrist_numbers["whitekingside"]
                    self.curr_hash ^= self.zobrist_numbers["whitequeenside"]
                else:
                    self.curr_hash ^= self.zobrist_numbers["blackkingside"]
                    self.curr_hash ^= self.zobrist_numbers["blackqueenside"]

    def _init_zobrist(self) -> dict:
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
        zobrist_numbers["whitekingside"] = random.getrandbits(bit_length)
        zobrist_numbers["whitequeenside"] = random.getrandbits(bit_length)
        zobrist_numbers["blackkingside"] = random.getrandbits(bit_length)
        zobrist_numbers["blackqueenside"] = random.getrandbits(bit_length)

        # each file has a hash if it is enpassant
        for file in chess.FILE_NAMES:
            zobrist_numbers[file] = random.getrandbits(bit_length)

        zobrist_numbers[chess.BLACK] = random.getrandbits(bit_length)

        return zobrist_numbers
    
    def _starting_zobrist_hash(self, zobrist_numbers: dict) -> int:
        board = chess.Board()
        z_hash = 0
        for square, piece in board.piece_map().items():
            z_hash ^= zobrist_numbers[(square, piece.piece_type, piece.color)]
        
        z_hash ^= zobrist_numbers["whitekingside"]
        z_hash ^= zobrist_numbers["whitequeenside"]
        z_hash ^= zobrist_numbers["blackkingside"]
        z_hash ^= zobrist_numbers["blackqueenside"]

        return z_hash


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
    

board = chess.Board()
print(format(board.castling_rights, "064b"))
print(board.ep_square)
zobrist_numbers = init_zobrist()
print(format(starting_zobrist_hash(zobrist_numbers), '064b'))