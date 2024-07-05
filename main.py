from tkinter import *
from tkinter import ttk

# Latest McGossy commit:
#TODO:
# Could probably use a code clean-up. We be feelin kind of noodly right now
# Connect AI and go brrrr
#
# I hate this reliance on globals. I guess it's probably good to get the AI to start thinking global strategy. But dang it's annoying
# Added buffers for end game states. On win/tie, click the board again to wipe it, or click button at bottom that declares game over state
# Added highlight to winning combo that resets with board
# Added all buttons to dictionary with their coordinates as the key IE: "0 1" "2 2" etc
#   I think this might be useful in doing a full restructure of the code if desired. As it's getting a little bit messy right now

# latest happysquid commit:
# TODO: nahh we dont need to rewrite this code, its a marvel of coding as a whole
#  too tired, but im gonna see how we could connect the AI to this

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

# Switches for turn, game over state & text, and the last winning cords
x_turn = True
game_over = False
game_over_text = StringVar()
winning_cords = []

# Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        global winning_cords
        #
        if game_over:
            for cords in winning_cords:
                all_game_buttons[f"{cords[0]} {cords[1]}"].configure(style="")
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
        global winning_cords
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
                    # Adds highlight to winning row
                    for cords in row_of_three:
                        all_game_buttons[f"{cords[0]} {cords[1]}"].configure(style="C.TButton")
                    winning_cords = row_of_three
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
        # Clears highlight
        for cords in winning_cords:
            all_game_buttons[f"{cords[0]} {cords[1]}"].configure(style="")


# Main setup of game board with main game loop
game_board = [[StringVar() for x in range(3)] for y in range(3)]
# Create dictionary with stringed out cords as the key, each button as the item
all_game_buttons = {}
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        all_game_buttons[f"{j} {i}"] = GameButton(mainframe, textvariable=game_board[j][i])

# grid each button
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        all_game_buttons[f"{i} {j}"].grid(row=i, column=j, ipadx=15, ipady=40)


# Bottom button for refreshing game board. Can only press if game state is WIN or TIE
bottom_frame = ttk.Frame(root, borderwidth=3)
bottom_frame.grid(column=0, row=1)
ttk.Button(bottom_frame, textvariable=game_over_text, command=button_wipe_game_board).grid(ipadx=90, ipady=20)

root.mainloop()