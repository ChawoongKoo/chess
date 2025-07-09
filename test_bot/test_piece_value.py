from engines.piece_value import value
import chess

def test_value() -> None:
    assert value(chess.PAWN) == 100.
    assert value(chess.KNIGHT) == 300.
    assert value(chess.BISHOP) == 300.
    assert value(chess.ROOK) == 500.
    assert value(chess.QUEEN) == 900.
    assert value(chess.KING) == 10000.