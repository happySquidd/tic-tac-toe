from tkinter import *
from tkinter import ttk

#ToDo
#Create valid winning states and a tie state
#Implement a turn system that switches between the letter 'X' and 'O'
#Don't allow a button to be pressed again if it's been pressed before (without switching turn)
#Connect AI and go brrrr

# latest happysquid commit:
# TODO: make it loop instead of quitting as it does now (erase squares and start over)
# TODO: imo it should wait for input to reset squares to show the board when tied or won
# TODO: or just create a reset button with condition text somewhere :D
# added a turn switch (to determine current turn)
# modified which letter is displayed/ added not allowing to switch already pressed button
# modified the check for a win condition and added a check for a tie (tie check could be improved. i cant think of a better way rn lmao)

#Setting up root window
root = Tk()
mainframe = ttk.Frame(root, borderwidth=3)
mainframe.grid(column=0, row=0)

# a switch to determine whose turn it is
x_turn = True


#Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, board, *args, **kwargs):
        super().__init__(board, *args, **kwargs)
        self.config(command=self.change_text)

    #Changes text of button to X or O, then calls check_win() to see if the move was a winning move
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

        print(f"{row} {column}")
        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                print(game_board[i][j].get(), end=' ')
            print()
        print("\n")

        self.check_tie_win()

    def check_tie_win(self):
        x_and_o = ['X', 'O']
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
        for e in x_and_o:
            for row_of_three in matrix:
                cords_1 = row_of_three[0]
                cords_2 = row_of_three[1]
                cords_3 = row_of_three[2]
                if game_board[cords_1[0]][cords_1[1]].get() == e and game_board[cords_2[0]][cords_2[1]].get() == e and game_board[cords_3[0]][cords_3[1]].get() == e:
                    # will quit on win change this so it stops and resets
                    print("WIN!")
                    root.quit()

        empty = 0
        for row in range(3):
            for btn in range(3):
                if game_board[row][btn].get() == '':
                    empty += 1

        if empty == 0:
            # will quit on tie
            print('Tie')
            root.quit()



game_board = [[StringVar() for x in range(3)] for y in range(3)]
# Makes a 3x3 board of buttons and places them into the mainframe
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        GameButton(mainframe, textvariable=game_board[j][i]).grid(column=i, row=j, ipadx=15, ipady=40)

root.mainloop()

