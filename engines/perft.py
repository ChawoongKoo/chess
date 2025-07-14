import chess
import os

def perft(board: chess.Board, depth: int) -> int:
    if depth == 0: return 1
    num_moves = 0
    for move in board.legal_moves:
        board.push(move)
        num_moves += perft(board, depth-1)
        board.pop()
    
    return num_moves

def run_perft(use_input: bool, fen = None):
    if use_input:
        os.system("clear")
        if fen:
            board = chess.Board(fen=fen)
        else:
            board = chess.Board()
        depth = int(input("Enter depth to search (# Plys): "))
        print(f"Searching to a depth of {depth}...")
        print(perft(board, depth))
    else:
        if fen:
            board = chess.Board(fen=fen)
        else:
            board = chess.Board()
        for depth in range(6):
            print(f"{depth}: {perft(board, depth)}")