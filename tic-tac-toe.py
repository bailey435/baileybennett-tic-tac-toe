import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Variables to track the game state
player_turn = "X"
game_board = [""] * 9
winner = None
score_X = 0
score_O = 0
is_vs_computer = False  # Flag for Player vs Computer mode
game_active = True  # Flag to prevent moves during computer's turn or after game ends

# Function to start the game (from the main menu)
def start_game(vs_computer=False):
    global is_vs_computer
    is_vs_computer = vs_computer  # Set the game mode
    main_menu_frame.pack_forget()  # Hide the main menu
    game_frame.pack()  # Show the game board
    reset_game()

# Function to go back to the main menu
def go_back_to_main_menu():
    game_frame.pack_forget()  # Hide the game board
    main_menu_frame.pack()  # Show the main menu
    reset_game()  # Reset the board for a new game

# Function to reset the game
def reset_game():
    global player_turn, game_board, winner, game_active
    player_turn = "X"
    game_board = [""] * 9
    winner = None
    game_active = True
    for button in buttons:
        button.config(text="", state="normal")
    update_turn_indicator()

# Function to check for a win or draw
def check_win():
    global winner, game_active
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
                      (0, 4, 8), (2, 4, 6)]  # diagonals

    for condition in win_conditions:
        if game_board[condition[0]] == game_board[condition[1]] == game_board[condition[2]] != "":
            winner = game_board[condition[0]]
            announce_winner()
            return True

    if "" not in game_board:  # Draw condition
        messagebox.showinfo("Draw", "It’s a Draw!")
        reset_game()
        return True
    return False

# Function to announce the winner
def announce_winner():
    global winner, game_active
    messagebox.showinfo("Winner", f"Congratulations! Player {winner} wins!")
    update_score()
    game_active = False
    reset_game()

# Function to update the score
def update_score():
    global score_X, score_O
    if winner == "X":
        score_X += 1
    elif winner == "O":
        score_O += 1
    score_label.config(text=f"Player X: {score_X} | Player O: {score_O}")

# Function to handle player moves
def button_click(index):
    global player_turn, game_active
    if buttons[index]["text"] == "" and winner is None and game_active:
        if player_turn == "X" or not is_vs_computer:  # Human player can only move when it's their turn
            buttons[index]["text"] = player_turn
            game_board[index] = player_turn
            if check_win() is False:
                player_turn = "O" if player_turn == "X" else "X"
                update_turn_indicator()
                if is_vs_computer and player_turn == "O":  # If vs computer and it's the computer's turn
                    root.after(500, computer_move)  # Delay computer move by 500ms

# Function to update the turn indicator
def update_turn_indicator():
    turn_label.config(text=f"Player {player_turn}'s Turn")

# Improved Minimax-based computer move
def computer_move():
    global player_turn, game_active
    best_move = find_best_move(game_board)
    game_board[best_move] = player_turn
    buttons[best_move].config(text=player_turn)
    if check_win() is False:
        player_turn = "X"
        update_turn_indicator()
    game_active = True  # Reactivate the game for the player after the computer's move

# Function to find the best move using Minimax
def find_best_move(board):
    best_value = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == "":  # Check only empty spots
            board[i] = "O"  # Try the move for computer
            move_value = minimax(board, 0, False)
            board[i] = ""  # Undo the move
            if move_value > best_value:
                best_value = move_value
                best_move = i
    return best_move

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    # Terminal states: someone has won or the board is full
    if score == 10:  # AI wins
        return score - depth  # Subtract depth to prioritize faster wins
    if score == -10:  # Human wins
        return score + depth  # Add depth to delay human victory
    if "" not in board:  # Draw
        return 0

    if is_maximizing:
        best_value = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best_value = max(best_value, minimax(board, depth + 1, False))
                board[i] = ""
        return best_value
    else:
        best_value = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best_value = min(best_value, minimax(board, depth + 1, True))
                board[i] = ""
        return best_value

# Function to evaluate the current board state
def evaluate(board):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
                      (0, 4, 8), (2, 4, 6)]  # diagonals

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]]:
            if board[condition[0]] == "O":
                return 10  # AI wins
            elif board[condition[0]] == "X":
                return -10  # Human wins
    return 0  # No one has won yet

# Main menu setup
main_menu_frame = tk.Frame(root)
main_menu_label = tk.Label(main_menu_frame, text="Tic-Tac-Toe", font="Helvetica 20 bold")
main_menu_label.pack(pady=20)

start_pvp_button = tk.Button(main_menu_frame, text="Player vs Player", font="Helvetica 15", command=lambda: start_game(False))
start_pvp_button.pack(pady=10)

start_pvc_button = tk.Button(main_menu_frame, text="Player vs Computer", font="Helvetica 15", command=lambda: start_game(True))
start_pvc_button.pack(pady=10)

exit_button = tk.Button(main_menu_frame, text="Exit", font="Helvetica 15", command=root.quit)
exit_button.pack(pady=10)

main_menu_frame.pack()

# Game board setup
game_frame = tk.Frame(root)

buttons = []
for i in range(9):
    button = tk.Button(game_frame, text="", font="Helvetica 20 bold", width=5, height=2,
                       command=lambda i=i: button_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Turn Indicator and Reset Button
turn_label = tk.Label(game_frame, text="Player X's Turn", font="Helvetica 15 bold")
turn_label.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(game_frame, text="Reset", font="Helvetica 15", command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3)

# Go Back to Main Menu Button
main_menu_button = tk.Button(game_frame, text="Main Menu", font="Helvetica 15", command=go_back_to_main_menu)
main_menu_button.grid(row=5, column=0, columnspan=3)

# Scoreboard Label
score_label = tk.Label(game_frame, text="Player X: 0 | Player O: 0", font="Helvetica 15")
score_label.grid(row=6, column=0, columnspan=3)

# Prevent resizing for consistent visual design
root.resizable(False, False)

# Start the Tkinter event loop
root.mainloop()
