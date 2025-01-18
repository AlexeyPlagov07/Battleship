import random
import os
import time

position = ['H', 'V']
columns = 'ABCDEFGHIJ'
pos_list = []  # All ship positions
ship_list = {'Carrier': 5, 'Battleship': 4, 'Destroyer': 3, 'Submarine': 3, 'Patrol': 2}
ship_count = {'Carrier': 0, 'Battleship': 0, 'Destroyer': 0, 'Submarine': 0, 'Patrol': 0}
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board_fin):    
    print('     A    B    C    D    E    F    G    H    I    J')
    for i in range(len(board_fin)):
        if i == 9:
            print(i+1, board_fin[i])
        else:
            print(i+1,'', board_fin[i])

def rand_ships():
    global pos_list
    pos_list = []
    global ship_pos_list
    ship_pos_list = {}

    for ship_name, ship_size in ship_list.items():
        repeat = True
        while repeat:
            temp_pos_list = []
            repeat = False
            col_start = random.choice(columns)
            row_start = random.randint(1, 10)
            orient = random.choice(position)

            if orient == 'V':
                if row_start + ship_size - 1 > 10:
                    row_end = row_start - (ship_size - 1)
                else:
                    row_end = row_start + (ship_size - 1)
                col_end = col_start
                for j in range(min(row_end, row_start), max(row_end, row_start) + 1):
                    if (col_end + str(j)) in pos_list:
                        repeat = True
                        break
                    else:
                        temp_pos_list.append(col_end + str(j))
            elif orient == 'H':
                row_end = row_start
                try:
                    col_end = columns[columns.index(col_start) + (ship_size - 1)]
                except IndexError:
                    col_end = columns[columns.index(col_start) - (ship_size - 1)]
                for j in range(min(columns.index(col_end), columns.index(col_start)),
                               max(columns.index(col_end), columns.index(col_start)) + 1):
                    if (columns[j] + str(row_end)) in pos_list:
                        repeat = True
                        break
                    else:
                        temp_pos_list.append(columns[j] + str(row_end))

        for h in temp_pos_list:
            ship_pos_list[h] = ship_name
        pos_list.extend(temp_pos_list)


def attack():
    hit = False
    guessed_positions = set()  # Track all guessed positions (hits and misses)
    last_hit = None  # To store the position of the last hit
    directions_to_check = []  # To store the directions of hunt (up, down, left, right)
    def check_sunk():
        if ship_count['Carrier'] == 5:
            print('SUNK!!!')
            ship_count['Carrier'] = 6
        elif ship_count['Battleship'] == 4:
            print('SUNK!!!')
            ship_count['Battleship'] = 6
        elif ship_count['Destroyer'] == 3:
            print('SUNK!!!')
            ship_count['Destroyer'] = 6
        elif ship_count['Submarine'] == 3:
            print('SUNK!!!')
            ship_count['Submarine'] = 6
        elif ship_count['Patrol'] == 2:
            print('SUNK!!!')
            ship_count['Patrol'] = 6
    def guess(hit, last_hit, directions_to_check):
        if hit and last_hit:  # If the last shot was a hit, try to guess surrounding positions
            row, col = int(last_hit[1:]), last_hit[0]
            row = int(row) - 1  # Adjust to 0-based index
            col = columns.index(col)
            
            # Add possible directions to check (up, down, left, right)
            if not directions_to_check:
                directions_to_check.extend([  # Initialize directions
                    (row - 1, col),  # Up
                    (row + 1, col),  # Down
                    (row, col - 1),  # Left
                    (row, col + 1)   # Right
                ])

            # Try the next direction from directions_to_check
            while directions_to_check:
                r, c = directions_to_check.pop(0)
                if 0 <= r < 10 and 0 <= c < 10:  # Check if the position is within bounds
                    spot = columns[c] + str(r + 1)
                    if spot not in guessed_positions:  # Only add valid and unguessed spots
                        return spot
        else:
            # Random guess during the hunt phase
            return get_random_spot()

    def get_random_spot():
        spot = f"{random.choice(columns)}{random.randint(1, 10)}"
        while spot in guessed_positions:  # Keep trying until we get a new spot
            spot = f"{random.choice(columns)}{random.randint(1, 10)}"
        return spot

    while [ship_count['Carrier'], ship_count['Battleship'], ship_count['Destroyer'], ship_count['Submarine'],
           ship_count['Patrol']] != [6, 6, 6, 6, 6]:
        spot = guess(hit, last_hit, directions_to_check)
        guessed_positions.add(spot)
        time.sleep(0.05)
        print(f"Enter Cell (ex: G7, F4, etc.): {spot}")
        if spot == None:
            spot = f'{random.choice(columns)}{random.randint(1,10)}'
        row = int(spot[1:]) - 1
        column = columns.index(spot[0])
        clear()
        if spot in pos_list:
            board[row][column] = "O"
            print_board(board)
            print("Hit!")
            hit = True
            ship_count[ship_pos_list[spot]] += 1
            last_hit = spot  # Store the hit position to target surrounding cells
            directions_to_check.clear()  # Reset direction stack on a hit
            check_sunk()
        else:
            board[row][column] = "X"
            print_board(board)
            print("Miss")
            hit = False
            check_sunk()
            # If miss, go back to the last known hit and try again in a different direction
            if last_hit:
                directions_to_check = [
                    (int(last_hit[1:]) - 2, columns.index(last_hit[0])),  # Up
                    (int(last_hit[1:]), columns.index(last_hit[0]) - 1),  # Left
                    (int(last_hit[1:]) - 1, columns.index(last_hit[0]) + 1),  # Right
                    (int(last_hit[1:]), columns.index(last_hit[0]) + 1)  # Down
                ]  # Reset directions to check after miss


rand_ships()
print_board(board)
attack()
print('YOU WON!!!')
