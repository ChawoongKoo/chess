import chess

values = {
    chess.PAWN: 100.,
    chess.BISHOP: 300.,
    chess.KNIGHT: 300.,
    chess.ROOK: 500.,
    chess.QUEEN: 900.,
    chess.KING: 10000.
}

def value(piece: chess.PieceType) -> float:
    return values[piece]