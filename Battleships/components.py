from random import randint, choice
import json

#Creates an empty 10x10 board and returns it
def initialise_board(size = 10):
    #empty list for board to be appended to
    starting_board = []
    #loops 10 times
    for counter in range(size):
        #empty list for row to be stored in
        row = []
        #loops 10 in an indented for loop
        for counter in range(size):
            #appends None to every item in the row
            row.append(None)
        #appends the row full of empty items
        starting_board.append(row)
    #returns empty list
    return starting_board

#reads a file full of battleships and creates a dictionary
def create_battleships(filename = "battleships.txt"):
    #opens the file "battleships.txt"
    file = open(filename, encoding="utf-8")
    file_contents = file.read()
    #splits up the lines by the commas
    lines = file_contents.split(',')
    my_dict = {}

    #loops thorugh each line
    for line in lines:
        #in each line there is a key and value split by a colon
        key, value = line.split(':')
        #adds the key and value to the dictionary
        my_dict[key.strip()] = value.strip()

    #makes every value in the dictionary an integer
    my_dict = {k: int(v) for k, v in my_dict.items()}
    #returns the battleships
    return my_dict

#places battleships on a 10 by 10 list of lists
def place_battleships(board, ships, algorithm = 'simple'):
    #selects which algorithm to use
    if algorithm == 'custom':
        #this is the order the ships health appear in the json file
        ship_health = [5, 4, 3, 3, 2]
        i = 0
        for ship, coordinates in ships.items():
            #loops through each ship in the dictionary
            segments = ship_health[i]
            #segments used to know how long to make each ship
            x = int(coordinates[0])
            y = int(coordinates[1])
            
            for j in range(segments):
                #loops based on ship size
                if coordinates[2] == "h":
                    #determines orientation then inserts ship name into board
                    board[x][y] = ship
                    x += 1
                else:
                    board[x][y] = ship
                    y += 1
            i += 1
        return board
    
    elif algorithm == 'random':
        #places battleships in random rows
        rows = list(range(0, 10))

        for key in ships:
            #loops through each ship
            segments = int(ships[key])
            #segments determine how long the ship is
            random_integer = randint(0,10-segments)
            #gets a random integer from 0 to 9
            random_row = choice(rows)
            #chooses a random row
            for i in range(segments):
                #based on size of the ship
                board[random_row][i+random_integer] = key
                #places the ship in a random row in a random place in the row
            rows.remove(random_row)
            #removes the row to stop overlap
        #returns list of lists with ships placed
        return board
    
    elif algorithm == 'simple':
        #places ships row by row
        row = 0
        for key in ships:
            #goes through each ship
            segments = int(ships[key])
            for i in range(segments):
                #places ship 1 by 1
                board[row][i] = key
            row += 1
        #returns list of lists of ships placed
        return board            

def read_placement(filename = "placement.json"):
    #reads json file
    f = open(filename, 'r')
    #opens file
    data = json.load(f)
    #stores whats inside
    f.close()
    #closes the file
    #returns what was inside the file
    return data