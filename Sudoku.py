import tkinter as tk
from tkinter import ttk
from tkinter import Button, Label, Entry, Listbox, Canvas, BooleanVar, IntVar, DoubleVar, filedialog, simpledialog, Checkbutton, Menu, messagebox, Scale, Radiobutton, OptionMenu, StringVar
from tkinter.ttk import Notebook, Frame, Treeview, PanedWindow

import numpy as np
from math import floor

anchor_x = 10
anchor_y = 10

square_size = 50

def create_game_board(canvas):
    i = anchor_x
    while i < 9 * square_size + anchor_x:    
        j = anchor_y
        while j < 9 * square_size + anchor_y:
            canvas.create_rectangle(i, j, i + square_size, j + square_size)
            
            j = j + square_size
        
        i = i + square_size
        
    draw_outer_lines(canvas)
    
    game_board = np.zeros((9, 9))

    return game_board

def draw_outer_lines(canvas):
    canvas.create_line(anchor_x + 3 * square_size, anchor_y, anchor_x + 3 * square_size, anchor_y + 9 * square_size, width = 3)
    canvas.create_line(anchor_x + 6 * square_size, anchor_y, anchor_x + 6 * square_size, anchor_y + 9 * square_size, width = 3)

    canvas.create_line(anchor_x, anchor_y + 3 * square_size, anchor_x + 9 * square_size, anchor_y + 3 * square_size, width = 3)
    canvas.create_line(anchor_x, anchor_y + 6 * square_size, anchor_x + 9 * square_size, anchor_y + 6 * square_size, width = 3)
    
    canvas.create_rectangle(anchor_x, anchor_y, anchor_x + 9 * square_size, anchor_y + 9 * square_size, width = 3)
        
#If override is None, simply toggle the highlight. Otherwise, set it to override
def highlight_square(canvas, highlights, square_x, square_y, override = None):
    highlights[square_x][square_y] = override if override is not None else not highlights[square_x][square_y]

    square_fill = "#bae3e3" if highlights[square_x][square_y] == True else "white"
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

def reset_highlights(canvas, highlights):
    for i in range(0, 9):
        for j in range(0, 9):
            if highlights[i][j]:
                highlight_square(canvas, highlights, i, j, False)

def right_click(event, canvas):
    square_x = floor((event.x - anchor_x) / square_size)
    square_y = floor((event.y - anchor_y) / square_size)
    
    if 0 <= square_x <= 9 and 0 <= square_y <= 9:
        reset_highlights(canvas, highlights)
        highlight_row(canvas, highlights, square_y)
        highlight_column(canvas, highlights, square_x)
        

root = tk.Tk()
root.title("Sudoku")

canvas_size = anchor_x + anchor_y + 9 * square_size
main_canvas = Canvas(root, bg = "white", height = canvas_size, width = canvas_size)

root.bind("<Button-3>", lambda event, arg = main_canvas: right_click(event, arg))

game_board = create_game_board(main_canvas)

#We'll use this array to keep track of highlighted tiles
highlights = np.zeros((9, 9))

highlight_row(main_canvas, highlights, 2)
highlight_column(main_canvas, highlights, 2)
reset_highlights(main_canvas, highlights)
#highlight_square(main_canvas, highlights, 4, 2)


main_canvas.pack()

root.mainloop()




