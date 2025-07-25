import chess

values = {
    chess.PAWN: 1.,
    chess.BISHOP: 3.,
    chess.KNIGHT: 3.,
    chess.ROOK: 5.,
    chess.QUEEN: 9.,
    chess.KING: 200.
}

def value(piece: chess.PieceType | None) -> float:
    if piece is None:
        raise Exception("Value function passed a piece with no value")
    return values[piece]