import numpy as np
import random
import tkinter as tk
from tkinter import font


def init_board(N):
    if N == -1:
        game_board = [[2,6,5,9,3,4,7,9,6],
                    [2,6,8,4,8,9,5,4,3],
                    [5,4,6,8,2,2,4,5,8],
                    [1,5,3,2,5,7,8,4,4],
                    [9,7,5,3,5,6,7,8,4],
                    [9,5,8,1,7,8,2,8,9],
                    [2,2,6,1,9,5,8,8,7],
                    [1,9,5,8,8,1,5,7,8],
                    [2,8,5,3,4,7,4,6,8]]
    else: 
        game_board = np.random.randint(1,9,(N,N),int)

    cell_groups=[]

    # Add rows
    for i in range(N):
        cell_groups.append([[i,j] for j in range(N)])
        
    # Add columns
    for j in range(N):
        cell_groups.append([[i,j] for i in range(N)])

    # Load other group cells
    loaded_data = np.load('data' + str(N) +'.npy')
    
    other_groups_board = loaded_data[random.randint(0,len(loaded_data)-1)]

    for number in range(1,N+1):
        cell_group=[]
        for i in range(N):
            for j in range(N):
                if other_groups_board[i][j]==number:
                    cell_group.append([i,j])
        cell_groups.append(cell_group)

    # cell_groups.append([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[3,0],[4,0]])
    # cell_groups.append([[0,3],[0,4],[0,5],[0,6],[1,3],[1,5],[1,6],[2,5],[2,6]])
    # cell_groups.append([[0,7],[0,8],[1,7],[1,8],[2,7],[2,8],[3,6],[3,7],[3,8]])
    # cell_groups.append([[1,4],[2,1],[2,2],[2,3],[2,4],[3,1],[3,2],[4,1],[4,2]])
    # cell_groups.append([[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]])
    # cell_groups.append([[4,6],[4,7],[5,6],[5,7],[6,4],[6,5],[6,6],[6,7],[7,4]])
    # cell_groups.append([[4,8],[5,8],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]])
    # cell_groups.append([[5,0],[5,1],[5,2],[6,0],[6,1],[7,0],[7,1],[8,0],[8,1]])
    # cell_groups.append([[6,2],[6,3],[7,2],[7,3],[7,5],[8,2],[8,3],[8,4],[8,5]])

    game_solution = np.random.choice(a=[False, True], size=(N,N))
    cell_groups_sums = []
    for group in cell_groups:
        cell_group_sum = 0
        for cell in group:
            if game_solution[cell[0]][cell[1]]:
                cell_group_sum += game_board[cell[0]][cell[1]]
        cell_groups_sums.append(int(cell_group_sum)) 
    

    # print(game_board,'\n\n', game_solution,'\n\n',other_groups_board,'\n\n',
    #       cell_groups_sums[0:N],'\n',cell_groups_sums[N:2*N],'\n',cell_groups_sums[2*N:3*N],'\n\n')
    return game_board, cell_groups, cell_groups_sums, game_solution



def is_possible_to_sum(target_sum, number_list):
    if target_sum < 0:
        return False
    if len(number_list)==0:
        if target_sum == 0:
            return True
        if target_sum != 0:
            return False
    return is_possible_to_sum(target_sum - number_list[0], number_list[1:]) or\
            is_possible_to_sum(target_sum, number_list[1:])

def update_game_board(my_solution, game_board, cell_groups, cell_group_sum, current_groups_sums, group_index, game_solution):
    # Rule 1
    for cell in cell_groups[group_index]:
        if my_solution[cell[0]][cell[1]] == 0 and game_board[cell[0]][cell[1]] + current_groups_sums[group_index] > cell_group_sum:
            my_solution[cell[0]][cell[1]] = 2
            text = 'Target sum: ' + str(cell_group_sum) +' Current sum: ' + str(current_groups_sums[group_index])+ '\nThe number '+\
                   str(game_board[cell[0]][cell[1]])+ ' can\'t be part of the solution.'
            assert not game_solution[cell[0]][cell[1]], "ERROR!!!!"
            return [cell, text]
    # Rule 2
    unset_cells=[cell for cell in cell_groups[group_index] if my_solution[cell[0]][cell[1]]==0]
    for i in range(len(unset_cells)):
        cell = unset_cells[i]
        if not is_possible_to_sum(cell_group_sum - current_groups_sums[group_index] - game_board[cell[0]][cell[1]], [game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]):
            my_solution[cell[0]][cell[1]] = 2
            text = 'Target sum: ' + str(cell_group_sum) + ' Current sum: '+ str(current_groups_sums[group_index])+ '\nThe number '+\
                   str(game_board[cell[0]][cell[1]])+ ' can\'t be part of the solution because ' + \
                   str(cell_group_sum - current_groups_sums[group_index] - game_board[cell[0]][cell[1]]) +\
                   ' can\'t be reached using '+\
                   str([int(game_board[cell[0]][cell[1]]) for cell in unset_cells[:i]+unset_cells[i+1:]])
            
            assert not game_solution[cell[0]][cell[1]], "ERROR!!!!"
            return [cell, text]
        if not is_possible_to_sum(cell_group_sum - current_groups_sums[group_index], [game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]):
            my_solution[cell[0]][cell[1]] = 1
            text = 'Target sum: '+ str(cell_group_sum) + ' Current sum: ' + str(current_groups_sums[group_index]) + ' \nThe number ' +\
            str(game_board[cell[0]][cell[1]]) + ' must be part of the solution because ' +\
            str(cell_group_sum - current_groups_sums[group_index])+\
            ' can\'t be reached using '+\
            str([int(game_board[cell[0]][cell[1]]) for cell in unset_cells[:i]+unset_cells[i+1:]])
            for j in range(len(cell_groups)):
                if cell in cell_groups[j]:
                    current_groups_sums[j] += game_board[cell[0]][cell[1]]

            assert game_solution[cell[0]][cell[1]], "ERROR!!!!"
            return [cell, text]
    return []


def print_board(game_board, cell_groups, cell_groups_sums, my_solution, cell, explanation_text, root, mistakes, hints):
    for widget in root.winfo_children():
        widget.destroy()
    N = len(game_board)
    cell_width = 40
    cell_height = 40

    canvas_width = (N + 1) * cell_width
    canvas_height = (N + 1) * cell_height

    main_frame = tk.Frame(root)
    main_frame.pack()

    canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(side="left")

    board_font = font.Font(family="Helvetica", size=12, weight="bold")

    colors = [
        "#FFCCCC", "#FFE5CC", "#FFFFCC", "#CCFFCC", "#CCCCFF",
        "#E5CCFF", "#FFCCE5", "#F0F0F0", "#FFF0CC", "#CCFFFF"
    ]

    # Draw column sums
    for col in range(N):
        sum_val = cell_groups_sums[N + col]
        x = (col + 1) * cell_width + cell_width // 2
        y = cell_height // 2
        canvas.create_text(x, y, text=str(sum_val), font=board_font, fill='blue')

    # Draw row sums
    for row in range(N):
        sum_val = cell_groups_sums[row]
        x = cell_width // 2
        y = (row + 1) * cell_height + cell_height // 2
        canvas.create_text(x, y, text=str(sum_val), font=board_font, fill='green')

    # Draw cells
    for row in range(N):
        for col in range(N):
            x1 = (col + 1) * cell_width
            y1 = (row + 1) * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # Color using cell_groups
            for index in range(N):
                if [row, col] in cell_groups[2*N + index]:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=colors[index], outline='gray')
                    break

            if [row, col] == cell:
                canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='black', width=2)

            for index in range(N):
                if cell_groups[2*N + index][0] == [row, col]:
                    canvas.create_text(x1 + 6, y1 + 6, text=str(cell_groups_sums[2*N + index]),
                                       font=font.Font(family="Helvetica", size=6), fill='black')
                    break

            number = game_board[row][col]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            canvas.create_text(cx, cy, text=str(number), font=board_font, fill='black')

            value = my_solution[row][col]
            radius = min(cell_width, cell_height) // 3

            if value == 1:
                canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="blue", width=2)
            elif value == 2:
                canvas.create_line(cx - radius, cy - radius, cx + radius, cy + radius, fill="red", width=2)
                canvas.create_line(cx - radius, cy + radius, cx + radius, cy - radius, fill="red", width=2)

    explanation_label = tk.Label(root, text=explanation_text, font=("Helvetica", 10), fg="darkgreen",
                                 wraplength=canvas_width - 20, justify="left")
    explanation_label.pack(pady=10)
    result = {}

    # Function to handle canvas click
    def on_canvas_left_click(event):
        col_clicked = (event.x // cell_width) - 1
        row_clicked = (event.y // cell_height) - 1

        # Check if inside the grid
        if 0 <= row_clicked < N and 0 <= col_clicked < N:
            # print(f"User left-clicked cell: ({row_clicked}, {col_clicked})")
            # You can call another function or update something here
            result[0]= 'Left'
            result[1]=[row_clicked, col_clicked]
            root.quit()
            
    def on_canvas_right_click(event):
        col_clicked = (event.x // cell_width) - 1
        row_clicked = (event.y // cell_height) - 1

        # Check if inside the grid
        if 0 <= row_clicked < N and 0 <= col_clicked < N:
            # print(f"User right-clicked cell: ({row_clicked}, {col_clicked})")
            # You can call another function or update something here
            result[0]= 'Right'
            result[1]=[row_clicked, col_clicked]
            root.quit()

    canvas.bind("<Button-1>", on_canvas_left_click)
    canvas.bind("<Button-3>", on_canvas_right_click)
    def on_button_click():
        root.quit()

    button = tk.Button(main_frame, text="Hint", command=on_button_click)
    button.pack(side="right", padx=10)


    status_frame = tk.Frame(root)
    status_frame.pack(pady=5)

    mistakes_label = tk.Label(status_frame, text="Mistakes: "+str(mistakes), font=("Helvetica", 10))
    mistakes_label.pack(side="left", padx=10)

    hints_label = tk.Label(status_frame, text="Hints: "+str(hints), font=("Helvetica", 10))
    hints_label.pack(side="left", padx=10)

    root.mainloop()

    return result


def solve_game(game_board, cell_groups, cell_groups_sums, game_solution, root):
    N = len(game_board)
    my_solution = np.zeros((N, N), int)
    current_groups_sums = np.zeros(len(cell_groups), int)
    mistakes=0
    hints=0
    cell=[-1,-1]
    text=""

    while True:
        output = print_board(game_board, cell_groups, cell_groups_sums, my_solution, cell, text, root, mistakes, hints)

        if output != {}:
            right_left = output[0]
            cell = output[1]

            if right_left == 'Right':
                if game_solution[cell[0]][cell[1]]:
                    text="Error!"
                    mistakes+=1
                else:
                    my_solution[cell[0]][cell[1]]=2
                    text="Well done! \n Number "+ str(game_board[cell[0]][cell[1]]) +" doesn't belong to the solution."
            else:
                if game_solution[cell[0]][cell[1]]:
                    my_solution[cell[0]][cell[1]]=1
                    text="Well done! \n Number "+ str(game_board[cell[0]][cell[1]]) +" belongs to the solution."
                else:
                    text="Error!"
                    mistakes+=1   
        else:
            hints+=1
            for i in range(len(cell_groups)):
                hint_output = update_game_board(my_solution, game_board, cell_groups, cell_groups_sums[i], current_groups_sums, i, game_solution)
                if hint_output != []:
                    cell=hint_output[0]
                    text=hint_output[1]
                    # print(cell_groups_sums[:N])
                    # print(my_solution,'\n')
                    break

        if not any(0 in sublist for sublist in my_solution):
            break



N = 6
# N=random.randint(3,10)
game_board, cell_groups, cell_groups_sums, game_solution = init_board(N) 


root = tk.Tk()
root.title("Game Board")
size=70+50*N
root.geometry(f"{size}x{size+50}+200+100")

solve_game(game_board, cell_groups, cell_groups_sums, game_solution, root)


