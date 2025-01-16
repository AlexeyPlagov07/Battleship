import random
position = ['H','V']
columns = 'ABCDEFGHIJ'
pos_list = []
pos_dict = {}
ship_list = {'Carrier':5, 'Battleship':4, 'Destroyer':3, 'Submarine':3, 'Patrol':2}

board = [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

def print_board(board_fin):    
    print('     A    B    C    D    E    F    G    H    I    J')
    for i in range(len(board_fin)):
        if i == 9:
            print(i+1, board_fin[i])
        else:
            print(i+1,'', board_fin[i])
    

def rand_ships():
    pos_list = []
    for i in ship_list:
        repeat = 1
        while repeat == 1:  
            temp_pos_list = []
            repeat = 0
            col_start = random.choice(columns)
            row_start = random.randint(1,10)
            orient = random.choice(position)

            if orient == 'V':
                if row_start + 5 > 10:
                    row_end = row_start - (ship_list[i] - 1)
                else:
                    row_end = row_start + (ship_list[i] - 1)
                col_end = col_start
                for j in range(min(row_end,row_start),max(row_end,row_start)+1):
                    if (col_end+str(j)) in pos_list:
                        print('repeat')
                        repeat = 1
                    else:
                        temp_val = col_end+str(j)
                        temp_pos_list.append(temp_val)
                        

                    

            elif orient == 'H':
                row_end = row_start
                try:
                    col_end = columns[columns.index(col_start) + (ship_list[i] - 1)]
                except IndexError:
                    col_end = columns[columns.index(col_start) - (ship_list[i] - 1)]
                for j in range(min(columns.index(col_end),columns.index(col_start)),max(columns.index(col_end),columns.index(col_start))+1):
                    if (columns[j]+str(row_end)) in pos_list:
                        print('repeat')
                        repeat = 1
                    else:
                        temp_val = columns[j]+str(row_end)
                        temp_pos_list.append(temp_val)
                        

        for h in temp_pos_list:
            board_row = int(h[1::]) - 1
            board_column = columns.index(h[0])
            board[board_row][board_column] = i[0]
        
        pos_list = pos_list + temp_pos_list

        print(col_start+str(row_start), col_end+str(row_end), orient)
        print(pos_list)
        print_board(board)
rand_ships()

print_board(board)