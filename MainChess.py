import chess
import os

board = chess.Board()

while True:
    os.system("clear")
    print(board)
    user_input = input("Enter a move (or 'q' to quit): ")
    os.system("clear")

    if user_input.lower() == 'q':
        print("Exiting.")
        break

    print(f"You entered: {user_input}")
    try:
        move = chess.Move.from_uci(user_input)
        board.push(move)
        print(board)

        if(board.is_checkmate()):
            print("Checkmate!")
            break
    except:
        print("Please enter a move in UCI format.")

