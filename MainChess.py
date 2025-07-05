import chess
import os
import time

board = chess.Board()

# print(board.legal_moves)
# def random_move() -> chess.Move:


while True:
    os.system("clear")
    print(board)
    user_input = input("Enter a move (or 'q' to quit): ")
    os.system("clear")

    if user_input.lower() == 'q':
        print("Exiting.")
        time.sleep(1)
        os.system("clear")
        break

    print(f"You entered: {user_input}")
    try:
        move = board.push_san(user_input)
        print(board)

        if(board.is_checkmate()):
            print("Checkmate!")
            break
    except:
        print("Please enter a move in SAN format.")
        time.sleep(1.5)
