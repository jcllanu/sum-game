import numpy as np
import json

def next(cell, n):
    if cell[1]==n-1:
        return [cell[0]+1,0]
    return [cell[0],cell[1]+1]

def cell_is_valid(cell, n):
    return cell[0]>=0 and cell[1]>=0 and cell[0]<n and cell[1]<n

def visit(i, j, visited, component, current_solution,number):
    if visited[i][j]:
        return current_solution[i][j]==0
    visited[i][j]=True
    touches_zero=False
    if current_solution[i][j]==number:
        component.append([i,j])
        vectors = [[0,1],[0,-1],[1,0],[-1,0]]
        for vector in vectors:
            if cell_is_valid([i+vector[0],j+vector[1]], len(current_solution)):
                touches_zero = visit(i+vector[0], j+vector[1], visited, component, current_solution, number) or touches_zero
        return touches_zero

    if current_solution[i][j]==0:
        return True
    return False   

def connected_or_potentially_connected(number, current_solution):
    n = len(current_solution)
    visited=np.zeros(dtype=bool, shape=(n,n))
    components=[]
    component_touch_zero=[]
    for i in range(n):
        for j in range(n):
            if not visited[i][j] and current_solution[i][j]==number:
                component=[]
                component_touch_zero.append(visit(i, j, visited, component, current_solution, number))
                components.append(component)
    return len(components)<2 or all(component_touch_zero)
        

def impossible_continue_solution(current_solution, numbers_left, current_cell, n, max_number):
    potential_locks = [i + 1 for i in range(n) if numbers_left[i] > 0 and numbers_left[i] < n]
    for j in range(n):
        if j <= current_cell[1]:
            if current_solution[current_cell[0]][j] in potential_locks:
                potential_locks.remove(current_solution[current_cell[0]][j])
        elif current_cell[0] > 0:
            if current_solution[current_cell[0]-1][j] in potential_locks:
                potential_locks.remove(current_solution[current_cell[0]-1][j])
    
    if len(potential_locks)> 0:
        return True
    
    for i in range(1, max_number + 1):
        if not connected_or_potentially_connected(i, current_solution):
            return True
        
    # for i in range(n):
    #     if all([number==current_solution[i][0] and number!=0 for number in current_solution[i]]):
    #         return True
        
    # for j in range(n):
    #     if all(row[j] == current_solution[0][j] and current_solution[0][j]!=0 for row in current_solution):
    #         return True

    if current_cell[0]==n-1: 
        # Check if column current_cell[i] has all the numbers the same
        if all(row[current_cell[1]] == current_solution[0][current_cell[1]] for row in current_solution):
            return True
    if current_cell[1]==n-1:
        # Check if row current_cell[0] has all the numbers the same
        if all([number==current_solution[current_cell[0]][0] for number in current_solution[current_cell[0]]]):
            return True
    return False
            
            
                
def backtracking(current_cell, n, numbers_left, current_solution, solutions_list):
    if len(solutions_list) > 10000:
        return
    max_number=1
    while max_number <= n:
        if numbers_left[max_number-1]==n:
            break
        max_number+=1
    if max_number > n:
        max_number=n

    for i in range(1,max_number+1):
        current_solution[current_cell[0]][current_cell[1]] = i

        if numbers_left[i-1]>0:
            numbers_left[i-1]-=1
        else:
            continue
        
        if not impossible_continue_solution(current_solution, numbers_left, current_cell, n, max_number):
            if current_cell[0]== n-1 and current_cell[1]== n-1:
                if True: #check solution
                    solutions_list.append(current_solution)
                    print(len(solutions_list))
                    # print(current_solution,'\n')
                    return
            else:
                backtracking(next(current_cell, n), n, numbers_left.copy(), current_solution.copy(), solutions_list)
        
        numbers_left[i-1]+=1

groups=dict({})
for n in range(8,10):
    solutions_list=[]
    backtracking([0,0], n, [n]*n, np.zeros((n,n)),solutions_list)
    groups[n]=solutions_list
    print(str(n)+':', len(solutions_list))
    # Save
    data = np.array(solutions_list)
    np.save('data' + str(n) +'.npy', data)