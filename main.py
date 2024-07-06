from tkinter import *
from tkinter import ttk

# Latest McGossy commit:
#TODO:
# Connect AI and go brrrr
#
# Separated win and tie functions
# Took those functions out of Class since they're static
# Cleaned up comments and other areas of the code
# Changed the switches to be in a dictionary so there's no global calls
# Wanted to separate functions & class into its own file but everything is too interconnected for that tbh


# latest happysquid commit:
# TODO: nahh we dont need to rewrite this code, its a marvel of coding as a whole
#  too tired, but im gonna see how we could connect the AI to this

# Setting up root window
root = Tk()
# Used to change style of buttons to highlight winning set
style = ttk.Style(root)
style.map("C.TButton",
   foreground=[('!active', 'black'),('pressed', 'black'), ('active', 'black')],
    background=[ ('!active','green'),('pressed', 'green'), ('active', 'green')]
    )
mainframe = ttk.Frame(root, borderwidth=3)
mainframe.grid(column=0, row=0)

# Switches for turn, game over state & text, and the last winning cords
game_variable = {'x_turn': True, 'game_over': False, 'game_over_text': StringVar(), 'last_winning_cords': []}


def highlight_cords(status):
    for cords in game_variable['last_winning_cords']:
        all_game_buttons[f"{cords[0]} {cords[1]}"].configure(style="C.TButton") if status == 'add' \
            else all_game_buttons[f"{cords[0]} {cords[1]}"].configure(style="")


def wipe_game_board():
    if game_variable['game_over_text'].get() in ['WIN', 'TIE']:
        for row in game_board:
            for letter in row:
                letter.set('')
        game_variable['game_over'] = False
        game_variable['game_over_text'].set('')
        # Clears highlight
        highlight_cords('remove')


def print_board():
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            print(game_board[i][j].get(), end=' ')
        print()


def check_win():
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
            if win:
                game_variable['last_winning_cords'] = row_of_three
                highlight_cords('add')
                game_variable['game_over'] = True
                game_variable['game_over_text'].set('WIN')
                print("WIN")
                return "WIN"


def check_tie():
    for row in game_board:
        for letter in row:
            if letter.get() == '':
                return
    game_variable['game_over'] = True
    game_variable['game_over_text'].set('TIE')
    print("TIE")
    return "TIE"


# Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.change_text)

    # Changes text of button to X or O, then calls check_win() to see if the move was a winning move
    def change_text(self):
        if game_variable['game_over']:
            highlight_cords('remove')
            game_variable['game_over'] = False
            game_variable['game_over_text'].set('')
            wipe_game_board()
            return

        row = self.grid_info()['row']
        column = self.grid_info()['column']

        if game_board[row][column].get() != '':
            return print('space taken')

        if game_variable['x_turn']:
            game_board[row][column].set('X')
            game_variable['x_turn'] = False
        else:
            game_board[row][column].set('O')
            game_variable['x_turn'] = True

        print_board()

        if check_win() != 'WIN':
            check_tie()


# Background game board that dictates what button text is displayed
game_board = [[StringVar() for x in range(3)] for y in range(3)]
# Create dictionary with stringed out cords as the key, each button as the item
# Keys are : "0 1" "2 1" "0 0" etc
all_game_buttons = {}
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        all_game_buttons[f"{j} {i}"] = GameButton(mainframe, textvariable=game_board[j][i])
        all_game_buttons[f"{j} {i}"].grid(row=j, column=i, ipadx=15, ipady=40)

# Bottom button for refreshing game board. Can only press if game state is WIN or TIE
bottom_frame = ttk.Frame(root, borderwidth=3)
bottom_frame.grid(column=0, row=1)
ttk.Button(bottom_frame, textvariable=game_variable['game_over_text'], command=wipe_game_board).grid(ipadx=90, ipady=20)

root.mainloop()