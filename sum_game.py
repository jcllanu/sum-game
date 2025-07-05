import numpy as np

N = 9

def init_board():
    game_board = [[2,6,5,9,3,4,7,9,6],
                [2,6,8,4,8,9,5,4,3],
                [5,4,6,8,2,2,4,5,8],
                [1,5,3,2,5,7,8,4,4],
                [9,7,5,3,5,6,7,8,4],
                [9,5,8,1,7,8,2,8,9],
                [2,2,6,1,9,5,8,8,7],
                [1,9,5,8,8,1,5,7,8],
                [2,8,5,3,4,7,4,6,8]]

    cell_groups=[]

    # Add rows
    for i in range(N):
        cell_groups.append([[i,j] for j in range(N)])
        
    # Add columns
    for j in range(N):
        cell_groups.append([[i,j] for i in range(N)])

    # Add other group cells
    cell_groups.append([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[3,0],[4,0]])
    cell_groups.append([[0,3],[0,4],[0,5],[0,6],[1,3],[1,5],[1,6],[2,5],[2,6]])
    cell_groups.append([[0,7],[0,8],[1,7],[1,8],[2,7],[2,8],[3,6],[3,7],[3,8]])
    cell_groups.append([[1,4],[2,1],[2,2],[2,3],[2,4],[3,1],[3,2],[4,1],[4,2]])
    cell_groups.append([[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]])
    cell_groups.append([[4,6],[4,7],[5,6],[5,7],[6,4],[6,5],[6,6],[6,7],[7,4]])
    cell_groups.append([[4,8],[5,8],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]])
    cell_groups.append([[5,0],[5,1],[5,2],[6,0],[6,1],[7,0],[7,1],[8,0],[8,1]])
    cell_groups.append([[6,2],[6,3],[7,2],[7,3],[7,5],[8,2],[8,3],[8,4],[8,5]])

    cell_groups_sums = [26, 22, 20, 21,  8, 17, 22, 14, 17,
                        17, 13,  5, 16, 26, 26, 29, 14, 21,
                        6, 25, 28, 28, 18, 14, 24, 19,  5]
    
    return game_board, cell_groups, cell_groups_sums



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

def update_game_board(game_solution, game_board, cell_groups, cell_group_sum, current_groups_sums, group_index):
    # Rule 1
    for cell in cell_groups[group_index]:
        if game_solution[cell[0]][cell[1]] == 0 and game_board[cell[0]][cell[1]] + current_groups_sums[group_index] > cell_group_sum:
            game_solution[cell[0]][cell[1]] = 2
            print('Target sum:', cell_group_sum, 'Current sum:', current_groups_sums[group_index], '\nThe number',
                   game_board[cell[0]][cell[1]], 'can\'t be part of the solution')
            return True
    # Rule 2
    unset_cells=[cell for cell in cell_groups[group_index] if game_solution[cell[0]][cell[1]]==0]
    for i in range(len(unset_cells)):
        cell = unset_cells[i]
        if not is_possible_to_sum(cell_group_sum - current_groups_sums[group_index] - game_board[cell[0]][cell[1]], [game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]):
            game_solution[cell[0]][cell[1]] = 2
            print('Target sum:', cell_group_sum, 'Current sum:', current_groups_sums[group_index], '\nThe number',
                   game_board[cell[0]][cell[1]], 'can\'t be part of the solution because', 
                   cell_group_sum - current_groups_sums[group_index] - game_board[cell[0]][cell[1]],
                   'can\'t be reached using',
                   str([game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]))
            return True
        if not is_possible_to_sum(cell_group_sum - current_groups_sums[group_index], [game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]):
            game_solution[cell[0]][cell[1]] = 1
            print('Target sum:', cell_group_sum, 'Current sum:', current_groups_sums[group_index], '\nThe number',
            game_board[cell[0]][cell[1]], 'must be part of the solution because', 
            cell_group_sum - current_groups_sums[group_index],
            'can\'t be reached using',
            str([game_board[cell[0]][cell[1]] for cell in unset_cells[:i]+unset_cells[i+1:]]))
            for j in range(len(cell_groups)):
                if cell in cell_groups[j]:
                    current_groups_sums[j] += game_board[cell[0]][cell[1]]
            return True
    return False
        
game_solution = np.zeros((N,N), int)

game_board, cell_groups, cell_groups_sums = init_board()
current_groups_sums = np.zeros(len(cell_groups), int)

while True:
    for i in range(len(cell_groups)):
        if update_game_board(game_solution, game_board, cell_groups, cell_groups_sums[i], current_groups_sums, i):
            print(game_solution,'\n')
            break

    if not any(0 in sublist for sublist in game_solution):
        break