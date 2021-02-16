import tkinter as tk
from tkinter import ttk
from tkinter import Button, Label, Entry, Listbox, Canvas, BooleanVar, IntVar, DoubleVar, filedialog, simpledialog, Checkbutton, Menu, messagebox, Scale, Radiobutton, OptionMenu, StringVar
from tkinter.ttk import Notebook, Frame, Treeview, PanedWindow

import numpy as np
from math import ceil, floor

#Padding off the window. Wouldn't want the squares to render off the screen
anchor_x = 10
anchor_y = 10

square_size = 55

#The game board is a 9x9 grid of squares. Draw this grid on the canvas
def create_game_board(canvas):
    i = anchor_x
    
    #Sudoku is always 9x9. No need to change this
    while i < 9 * square_size + anchor_x:    
        j = anchor_y
        while j < 9 * square_size + anchor_y:
            canvas.create_rectangle(i, j, i + square_size, j + square_size)
            
            j = j + square_size
        
        i = i + square_size
        
    draw_outer_lines(canvas)
    
    game_board = np.zeros((9, 9))

    return game_board

#Because of overlapping when filling a rectangle, the thicker lines need to be drawn constantly.
#Thus, here's the function for it
def draw_outer_lines(canvas):
    #The thicker lines outline the 3x3 subgrids
    canvas.create_line(anchor_x + 3 * square_size, anchor_y, anchor_x + 3 * square_size, anchor_y + 9 * square_size, width = 3)
    canvas.create_line(anchor_x + 6 * square_size, anchor_y, anchor_x + 6 * square_size, anchor_y + 9 * square_size, width = 3)

    canvas.create_line(anchor_x, anchor_y + 3 * square_size, anchor_x + 9 * square_size, anchor_y + 3 * square_size, width = 3)
    canvas.create_line(anchor_x, anchor_y + 6 * square_size, anchor_x + 9 * square_size, anchor_y + 6 * square_size, width = 3)
    
    canvas.create_rectangle(anchor_x, anchor_y, anchor_x + 9 * square_size, anchor_y + 9 * square_size, width = 3)
        
#If override is None, simply toggle the highlight. Otherwise, set it to override
def highlight_square(canvas, highlights, square_x, square_y, color = "#cfffff", override = None):
    highlights[square_x][square_y] = override if override is not None else not highlights[square_x][square_y]

    square_fill = color if highlights[square_x][square_y] == True else "white"
    canvas.create_rectangle(anchor_x + square_x * square_size, anchor_y + square_y * square_size, anchor_x + (square_x + 1) * square_size, anchor_y + (square_y + 1) * square_size, fill = square_fill , outline = "black")

    draw_outer_lines(canvas)

def highlight_row(canvas, highlights, row):
    for j in range(0, 9):
        #We don't want to toggle off already highlighted squares here on accident
        highlight_square(canvas, highlights, j, row, override = True)

def highlight_column(canvas, highlights, column):
    for i in range(0, 9):
        #We don't want to toggle off already highlighted squares here on accident
        highlight_square(canvas, highlights, column, i, override = True)

def highlight_cross_section(canvas, highlights, row, column):
    highlight_row(canvas, highlights, column)
    highlight_column(canvas, highlights, row)
    
    #Highlight the central square a different color for pretty visualization
    highlight_square(canvas, highlights, row, column, color = "#8de6e6", override = True)

def highlight_sub_grid(canvas, highlights, row, column):
    #There's a good chance we accidentally use this function for a square rather than a subgrid
    if row > 2 or column > 2:
        raise ValueError("Row/Column index too high. Perhaps you're using the wrong function?")
    else:
        for i in range(0, 3):
            for j in range(0, 3):
                highlight_square(canvas, highlights, i + 3 * row, j + 3 * column, override = True)

#Set every highlight to False
def reset_highlights(canvas, highlights):
    for i in range(0, 9):
        for j in range(0, 9):
            if highlights[i][j]:
                highlight_square(canvas, highlights, i, j, override = False)

#Mathematically determine which square was clicked, then highlight the cross-section
def right_click(event, canvas):
    square_x = floor((event.x - anchor_x) / square_size)
    square_y = floor((event.y - anchor_y) / square_size)
    
    if 0 <= square_x <= 9 and 0 <= square_y <= 9:
        reset_highlights(canvas, highlights)
        highlight_cross_section(canvas, highlights, square_x, square_y)
        

root = tk.Tk()
root.title("Sudoku")

canvas_size = anchor_x + anchor_y + 9 * square_size
main_canvas = Canvas(root, bg = "white", height = canvas_size, width = canvas_size)

root.bind("<Button-3>", lambda event, arg = main_canvas: right_click(event, arg))

game_board = create_game_board(main_canvas)

#We'll use this array to keep track of highlighted tiles
highlights = np.zeros((9, 9))

#Testing code. Don't delete this guys, just comment it out until stuff is implemented
highlight_sub_grid(main_canvas, highlights, 1, 0)


temp = Label(root, text = "1   2   3\n4   5   6\n7   8   9", bg = "white")
#temp.config(font = ("TkDefaultFont", ceil(square_size / 2)))
temp.place(x = 0, y = 0)
root.update()

label_width = temp.winfo_width()
label_height = temp.winfo_height()

padding_x = (square_size - label_width) / 2
padding_y = (square_size - label_height) / 2

temp.place(x = anchor_x + padding_x + 2 * square_size, y = anchor_y + padding_y + 2 * square_size)

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

root.mainloop()




