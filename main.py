from tkinter import *
from tkinter import ttk

# Latest McGossy commit:
#TODO:
# Connect AI and go brrrr
#
# I hate this reliance on globals. I guess it's probably good to get the AI to start thinking global strategy. But dang it's annoying
# Added buffers for end game states. On win/tie, click the board again to wipe it, or click button at bottom that declares game over state
# Added a style map but that's only going to be useful if we can target buttons locationally and idk if that's possible
# Ideally I wanted to highlight the winning combo before we reset the board

# latest happysquid commit:
# TODO: make it loop instead of quitting as it does now (erase squares and start over)
# TODO: imo it should wait for input to reset squares to show the board when tied or won
# TODO: or just create a reset button with condition text somewhere :D
# added a turn switch (to determine current turn)
# modified which letter is displayed/ added not allowing to switch already pressed button
# modified the check for a win condition and added a check for a tie (tie check could be improved. i cant think of a better way rn lmao)

# Setting up root window
root = Tk()
# Only want to use style if we can figure out how to target buttons via location
# Will change style of winning buttons to this style using self.config(style="C.TButton")
style = ttk.Style(root)
style.map("C.TButton",
   foreground=[('!active', 'black'),('pressed', 'black'), ('active', 'black')],
    background=[ ('!active','green'),('pressed', 'green'), ('active', 'green')]
    )
mainframe = ttk.Frame(root, borderwidth=3)
mainframe.grid(column=0, row=0)

# a switch to determine whose turn it is
x_turn = True
game_over = False
game_over_text = StringVar()

# Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, board, *args, **kwargs):
        super().__init__(board, *args, **kwargs)
        self.config(command=self.change_text)

    # Might leave this in here for future auto-wiping
    def wipe_game_board(self):
        for row in game_board:
            for letter in row:
                letter.set('')

    # Changes text of button to X or O, then calls check_win() to see if the move was a winning move
    def change_text(self):
        global x_turn
        global game_over
        #
        if game_over:
            self.wipe_game_board()
            game_over = False
            game_over_text.set('')
            return

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
        global game_over
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
                    game_over = True
                    game_over_text.set('WIN')
                    print("WIN")
                    return "WIN"

        # Checks for tie
        for row in game_board:
            for letter in row:
                if letter.get() == '':
                    return

        game_over = True
        game_over_text.set('TIE')
        print("TIE")
        return "TIE"


# For bottom button
def button_wipe_game_board():
    global game_over
    if game_over_text.get() in ['WIN', 'TIE']:
        for row in game_board:
            for letter in row:
                letter.set('')
        game_over = False
        game_over_text.set('')


# Main setup of game board with main game loop
game_board = [[StringVar() for x in range(3)] for y in range(3)]
# Makes a 3x3 board of buttons and places them into the mainframe
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        GameButton(mainframe, textvariable=game_board[j][i]).grid(column=i, row=j, ipadx=15, ipady=40)

# Bottom button for refreshing game board. Can only press if game state is WIN or TIE
bottom_frame = ttk.Frame(root, borderwidth=3)
bottom_frame.grid(column=0, row=1)
ttk.Button(bottom_frame, textvariable=game_over_text, command=button_wipe_game_board).grid(ipadx=90, ipady=20)

root.mainloop()