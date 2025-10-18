import components as comp
def attack(coordinates, board, battleships):
    #checks coordinates and either hits or misses
    x, y = coordinates
    #x and y coordinates are seperated from tuple
    tile_type = board[x][y]
    #checks what kind of ship is being hit if there is any
    if tile_type is not None:
        #if it is not None then there is a ship there and it is hit
        print("hit")
        tile_type = str(tile_type)
        
        battleships[tile_type] = battleships[tile_type] - 1
        #decrements the ships health by 1
        board[x][y] = None
        #changes the tile to None as the ship segment has sank
        if battleships[tile_type] == 0:
        #when the ships health reaches 0 it is sank and it tells the player
            print("you have sunk a {}".format(tile_type))

        return True
        #returns True if a hit has occured, which it has if its running this code
    else:
        #if the tile is None then it is a miss
        print("miss")
        #returns False as it is a miss
        return False

def cli_coordinates_input():
    #asks user what coordinates it wants to hit and stores it in a tuple that has format (x, y)
    coordinates = input("enter where you want to attack in the for 'x,y'")
    #stores coordinates that the user inputs
    tup = coordinates.split(',')
    #splits up the x and y coordinates
    tup = tuple([int(x) for x in tup])
    #turns the x and y values into integers before putting them back in a tuple
    #returns the coordinates that are being attacked
    return tup

def simple_game_loop():
    #loops through a simple version of the game where the user attacks the enemy until they win
    print("welcome to the game")
    #initialises the game board to be used
    game_board = comp.place_battleships(comp.initialise_board(), comp.create_battleships(),'random')
    #initialises the opponents health
    health = comp.create_battleships()

    while sum(health.values()) != 0:
    #when the opponents health is 0 the while loop will end
        attack(cli_coordinates_input(), game_board, health)
        #calls the attack function
    print("game over")
    #prints when game is finished
    
if __name__ == '__main__':
    simple_game_loop()
