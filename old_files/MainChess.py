import chess
import os
import time
import random

board = chess.Board(fen="2k2q2/Q7/1K6/8/8/8/8/8 w - - 0 1")
print(board)
print(board.legal_moves)

def random_move() -> chess.Move:
    return random.choice(list(board.legal_moves))

while True:
    os.system("clear")
    print(board)
    if not board.turn:
        move = random_move()
        board.push(move)
        time.sleep(.5)
        continue
    print(f"\nWhite to move." if board.turn else "Black to move")
    user_input = input("Enter a move (or 'q' to quit): ")
    os.system("clear")

    if user_input.lower() == 'q':
        print("Exiting.")
        time.sleep(.5)
        os.system("clear")
        break

    print(f"You entered: {user_input}")
    try:
        move = board.push_san(user_input)
        print(board)

        outcome = board.outcome()
        if(outcome):
            print("Checkmate!")
            print(outcome.result())
            break
    except:
        print("Please enter a move in SAN format.")
        time.sleep(1.5)
