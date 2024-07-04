from tkinter import *
from tkinter import ttk

# Latest McGossy commit:
#TODO:
# Add pause before wiping screen / Reset button on game_over state
# Connect AI and go brrrr
#
# Set up returns for Win & Tie as I imagine that'll be helpful when we move forward with plugging the learning algorithm
# Added a function to wipe the board. Used on Win / Tie success
# Cleaned up Tie condition
# Made Win condition worse lmao
# 1st turn after a win is currently working on a "loser goes first" strategy. IE: X wins, O goes first next
# This is unintentional but idc if we keep it like that or not lol

# latest happysquid commit:
# TODO: make it loop instead of quitting as it does now (erase squares and start over)
# TODO: imo it should wait for input to reset squares to show the board when tied or won
# TODO: or just create a reset button with condition text somewhere :D
# added a turn switch (to determine current turn)
# modified which letter is displayed/ added not allowing to switch already pressed button
# modified the check for a win condition and added a check for a tie (tie check could be improved. i cant think of a better way rn lmao)

# Setting up root window
root = Tk()
mainframe = ttk.Frame(root, borderwidth=3)
mainframe.grid(column=0, row=0)

# a switch to determine whose turn it is
x_turn = True


# Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, board, *args, **kwargs):
        super().__init__(board, *args, **kwargs)
        self.config(command=self.change_text)

    # Literally just used for initial game_board setup lol. Won't work with assignment within class scope for game_board
    def create_blank_game_board():
        return [[StringVar() for x in range(3)] for y in range(3)]

    def wipe_game_board(self):
        for row in game_board:
            for letter in row:
                letter.set('')

    # Changes text of button to X or O, then calls check_win() to see if the move was a winning move
    def change_text(self):
        global x_turn
        row = self.grid_info()['row']
        column = self.grid_info()['column']

        if game_board[row][column].get() != '':
            return print('space taken')

        if x_turn:
            game_board[row][column].set('X')
            x_turn = False
        else:
            game_board[row][column].set('O')
            x_turn = True

        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                print(game_board[i][j].get(), end=' ')
            print()
        print("\n")

        self.check_win_tie()

    def check_win_tie(self):
        matrix = [  # horizontal
                  [[0, 0], [0, 1], [0, 2]],
                  [[1, 0], [1, 1], [1, 2]],
                  [[2, 0], [2, 1], [2, 2]],
                  # vertical
                  [[2, 0], [1, 0], [0, 0]],
                  [[2, 1], [1, 1], [0, 1]],
                  [[2, 2], [1, 2], [0, 2]],
                  # diagonal
                  [[2, 0], [1, 1], [0, 2]],
                  [[0, 0], [1, 1], [2, 2]]]
        for letter in ['X', 'O']:
            for row_of_three in matrix:
                win = True
                for cords in row_of_three:
                    if game_board[cords[0]][cords[1]].get() != letter:
                        win = False
                        break
                # Needs to return on win else a last move win will return win & tie
                if win:
                    self.wipe_game_board()
                    print("WIN")
                    return "WIN"

        # Checks for tie
        for row in game_board:
            for letter in row:
                if letter.get() == '':
                    return False

        self.wipe_game_board()
        print("TIE")
        return "TIE"


# Main setup of game board with main game loop
game_board = GameButton.create_blank_game_board()
# Makes a 3x3 board of buttons and places them into the mainframe
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        GameButton(mainframe, textvariable=game_board[j][i]).grid(column=i, row=j, ipadx=15, ipady=40)

root.mainloop()