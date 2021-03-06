import tkinter as tk
from tkinter import ttk
from tkinter import Button, Label, Entry, Listbox, Canvas, BooleanVar, IntVar, DoubleVar, filedialog, simpledialog, Checkbutton, Menu, messagebox, Scale, Radiobutton, OptionMenu, StringVar
from tkinter.ttk import Notebook, Frame, Treeview, PanedWindow

import numpy as np
from math import ceil, floor




class Sudoku:
    class Tile:
        def __init__(self, canvas, label):
            self.value = -1
            self.canvas = canvas
            self.label = label
            
            self.rect_id = -1
            
            self.notes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.display_notes(0)
            
        def draw(self, anchor_x, anchor_y, square_x, square_y, square_size, square_fill):
            self.label.config(bg = square_fill)
            if self.rect_id != -1:
                self.canvas.delete(self.rect_id)
                
            self.rect_id = self.canvas.create_rectangle(anchor_x + square_x * square_size, anchor_y + square_y * square_size, anchor_x + (square_x + 1) * square_size, anchor_y + (square_y + 1) * square_size, fill = square_fill , outline = "black")
        
        def display_notes(self, square_size):
            #Reset a couple of things
            self.label.config(font = ("TkDefaultFont",))
            self.value = -1
            
            count = 0
            for i in range(0, 9):
                if self.notes[i]:
                    count = count + 1
            
            if count == 0:
                #This is hard-coded. A space for each number, plus a 3-space gap
                self.label.config(text = "         \n         \n         ")
            
            elif count == 1:
                self.label.config(font = ("TkDefaultFont", ceil(square_size / 2)))   
                number = -1
                for i in range(0, 9):
                    if self.notes[i]:
                        number = i + 1

                self.value = number
                self.label.config(text = str(number))
                
            else:
                output = ""
                for i in range(0, 3):
                    for j in range(0, 3):
                        if self.notes[3 * i + j]:
                            output = output + str(3 * i + j + 1)
                        else:
                            output = output + " "
                        
                        if j != 2:
                            output = output + "   "
                    
                    if i != 2:
                        output = output + "\n"
                self.label.config(text = output)
          
    def __init__(self, root):
        self.root = root
    
        #Padding off the window. Wouldn't want the squares to render off the screen
        self.anchor_x = 10
        self.anchor_y = 10

        self.square_size = 55
        
        self.lines = []
        self.current_cross_section = None
        
        canvas_size = self.anchor_x + self.anchor_y + 9 * self.square_size
        self.canvas = Canvas(root, bg = "white", height = canvas_size, width = canvas_size)

        self.canvas.bind("<Button-1>", lambda event: self.right_click(event))
        
        for i in range(1, 10):
            self.root.bind(str(i), lambda event: self.number_pressed(event))
    
        self.root.bind("<Up>", lambda event: self.arrow_pressed(event))
        self.root.bind("<Left>", lambda event: self.arrow_pressed(event))
        self.root.bind("<Right>", lambda event: self.arrow_pressed(event))
        self.root.bind("<Down>", lambda event: self.arrow_pressed(event))
    
        self.canvas.pack()

        self.create_game_board()

    #Mathematically determine which square was clicked, then highlight the cross-section
    def right_click(self, event, root_widget = None):
        if root_widget != None:
            event.x = event.x + root_widget.winfo_x()
            event.y = event.y + root_widget.winfo_y()

        square_x = floor((event.x - self.anchor_x) / self.square_size)
        square_y = floor((event.y - self.anchor_y) / self.square_size)

        if 0 <= square_x <= 9 and 0 <= square_y <= 9:
            self.reset_highlights()
            self.highlight_cross_section(square_x, square_y)
            self.current_cross_section = (square_x, square_y)
            
    def number_pressed(self, event):
        if self.current_cross_section != None:
            x, y = self.current_cross_section
            key = int(event.char)
            self.game_board[x][y].notes[key - 1]= not self.game_board[x][y].notes[key - 1]
            self.game_board[x][y].display_notes(self.square_size)
            
            if self.game_board[x][y].value != -1:
                self.highlight_cross_sections_of_same_number(x, y)
            
    def arrow_pressed(self, event):
        if self.current_cross_section == None:
            x, y = (0, 0)
        else:
            if event.keysym == "Up" and self.current_cross_section[1] != 0:
                x, y = self.current_cross_section
                y = y - 1
            
            if event.keysym == "Left" and self.current_cross_section[0] != 0:
                x, y = self.current_cross_section
                x = x - 1
            
            if event.keysym == "Right" and self.current_cross_section[0] != 8:
                x, y = self.current_cross_section
                x = x + 1
            
            if event.keysym == "Down" and self.current_cross_section[1] != 9:
                x, y = self.current_cross_section
                y = y + 1
                
        self.current_cross_section = (x, y)
        self.reset_highlights()
        self.highlight_cross_section(x, y)
        
        if self.game_board[x][y].value != -1:
            self.highlight_cross_sections_of_same_number(x, y)

    
    #The game board is a 9x9 grid of squares. Draw this grid on the canvas
    def create_game_board(self):
        i = self.anchor_x
        
        #Sudoku is always 9x9. No need to change this
        while i < 9 * self.square_size + self.anchor_x:    
            j = self.anchor_y
            while j < 9 * self.square_size + self.anchor_y:
                self.canvas.create_rectangle(i, j, i + self.square_size, j + self.square_size)
                
                j = j + self.square_size
            
            i = i + self.square_size
            
        self.draw_outer_lines()
        
        self.game_board = np.zeros((9, 9), dtype = object)
        for i in range(0, 9):
            for j in range(0, 9):
                self.game_board[i][j] = self.create_tile(i, j)
        
        self.game_board[2][2].notes = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.game_board[2][2].display_notes(self.square_size)
        self.game_board[5][6].notes = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        self.game_board[5][6].display_notes(self.square_size)
        self.game_board[8][3].notes = [1, 0, 1, 1, 1, 0, 0, 0, 1]
        self.game_board[8][3].display_notes(self.square_size)
        self.highlights = np.zeros((9, 9))
    
    def create_tile(self, row, column):
        temp = Label(self.canvas, text = "0   0   0\n0   0   0\n0   0   0", bg = "white")
        
        x = self.square_size * row + self.anchor_x + (self.square_size - temp.winfo_reqwidth()) / 2
        y = self.square_size * column + self.anchor_y + (self.square_size - temp.winfo_reqheight()) / 2

        temp.place(x = x, y = y)
        temp.bind("<Button-1>", lambda event: self.right_click(event, temp))
        
        return self.Tile(self.canvas, temp)
        
        
    #Because of overlapping when filling a rectangle, the thicker lines need to be drawn constantly.
    #Thus, here's the function for it
    def draw_outer_lines(self):
        if self.lines != []:
            for line in self.lines:
                self.canvas.delete(line)
            self.lines = []
            
        #I'm not writing this 40 times
        anchor_x = self.anchor_x
        anchor_y = self.anchor_y
        square_size = self.square_size
        
        #The thicker lines outline the 3x3 subgrids
        self.lines.append(self.canvas.create_line(anchor_x + 3 * square_size, anchor_y, anchor_x + 3 * square_size, anchor_y + 9 * square_size, width = 3))
        self.lines.append(self.canvas.create_line(anchor_x + 6 * square_size, anchor_y, anchor_x + 6 * square_size, anchor_y + 9 * square_size, width = 3))

        self.lines.append(self.canvas.create_line(anchor_x, anchor_y + 3 * square_size, anchor_x + 9 * square_size, anchor_y + 3 * square_size, width = 3))
        self.lines.append(self.canvas.create_line(anchor_x, anchor_y + 6 * square_size, anchor_x + 9 * square_size, anchor_y + 6 * square_size, width = 3))
        
        self.lines.append(self.canvas.create_rectangle(anchor_x, anchor_y, anchor_x + 9 * square_size, anchor_y + 9 * square_size, width = 3))

    #If override is None, simply toggle the highlight. Otherwise, set it to override
    def highlight_square(self, square_x, square_y, color = "#cfffff", override = None):
        self.highlights[square_x][square_y] = override if override is not None else not self.highlights[square_x][square_y]

        square_fill = color if self.highlights[square_x][square_y] == True else "white"
        self.game_board[square_x][square_y].draw(self.anchor_x, self.anchor_y, square_x, square_y, self.square_size, square_fill)

        self.draw_outer_lines()
        
    def highlight_row(self, row):
        for j in range(0, 9):
            #We don't want to toggle off already highlighted squares here on accident
            self.highlight_square(row, j, override = True)

    def highlight_column(self, column):
        for i in range(0, 9):
            #We don't want to toggle off already highlighted squares here on accident
            self.highlight_square(i, column, override = True)

    def highlight_cross_section(self, row, column):
        self.highlight_row(row)
        self.highlight_column(column)
        
        #Highlight the central square a different color for pretty visualization
        self.highlight_square(row, column, color = "#8de6e6", override = True)
        
        self.highlight_cross_sections_of_same_number(row, column)
    
    def highlight_cross_sections_of_same_number(self, row, column):
        number = self.game_board[row][column].value

        #Not -1 implies no notes are on the tile
        if number != -1:
            for i in range(0, 9):
                for j in range(0, 9):
                    if self.game_board[i][j].value == number and i != row and j != column:
                        #Don't use highlight cross section here. This should be purely visual
                        self.highlight_row(i)
                        self.highlight_column(j)
                        

    def highlight_sub_grid(self, row, column):
        #There's a good chance we accidentally use this function for a square rather than a subgrid
        if row > 2 or column > 2:
            raise ValueError("Row/Column index too high. Perhaps you're using the wrong function?")
        else:
            for i in range(0, 3):
                for j in range(0, 3):
                    self.highlight_square(i + 3 * row, j + 3 * column, override = True)

    #Set every highlight to False
    def reset_highlights(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.highlights[i][j]:
                    self.highlight_square(i, j, override = False)

root = tk.Tk()
root.title("Sudoku")

sudoku = Sudoku(root)

#Testing code. Don't delete this guys, just comment it out until stuff is implemented
sudoku.highlight_sub_grid(1, 0)

'''


temp = Label(root, text = "5", bg = "white")
temp.config(font = ("TkDefaultFont", ceil(square_size / 2)))
temp.place(x = 0, y = 0)
root.update()

label_width = temp.winfo_width()
label_height = temp.winfo_height()

padding_x = (square_size - label_width) / 2
padding_y = (square_size - label_height) / 2

temp.place(x = anchor_x + padding_x + 1 * square_size, y = anchor_y + padding_y + 2 * square_size)
#Testing code ends here

main_canvas.pack()
'''
root.mainloop()




