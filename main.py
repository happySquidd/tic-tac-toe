from tkinter import *
from tkinter import ttk

#ToDo
#Create valid winning states and a tie state
#Implement a turn system that switches between the letter 'X' and 'O'
#Don't allow a button to be pressed again if it's been pressed before (without switching turn)
#Connect AI and go brrrr

#Setting up root window
root = Tk()
mainframe = ttk.Frame(root, borderwidth=3)
mainframe.grid(column=0, row=0)


#Custom button class that stores its location for switching button text
class GameButton(ttk.Button):
    def __init__(self, board, *args, **kwargs):
        super().__init__(board, *args, **kwargs)
        self.config(command=self.change_text)

    #Changes text of button to X or O, then calls check_win() to see if the move was a winning move
    def change_text(self):
        row = self.grid_info()['row']
        column = self.grid_info()['column']

        if game_board[row][column].get() == '':
            game_board[row][column].set('X')
        elif game_board[row][column].get() == 'X':
            game_board[row][column].set('O')
        elif game_board[row][column].get() == 'O':
            game_board[row][column].set('X')

        print(f"{row} {column}")
        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                print(game_board[i][j].get(), end=' ')
            print()
        print("\n\n")

        self.check_win()

    def check_win(self):
        if game_board[0][0].get() == 'X' and game_board[0][1].get() == 'X' and game_board[0][2].get() == 'X':
            print("WIN!")


global game_board
game_board = [[StringVar() for x in range(3)] for y in range(3)]
# Makes a 3x3 board of buttons and places them into the mainframe
for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        GameButton(mainframe, textvariable=game_board[j][i]).grid(column=i, row=j, ipadx=15, ipady=40)

root.mainloop()

