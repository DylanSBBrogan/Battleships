import numpy as np
import components as comp
import game_engine as gm

rng = np.random.default_rng()
#initialises random integers

players = {}
#stores a global dictionary for player
#and opponent game information to be stored in

def generate_attack():
    #creates random coordinates for an attack
    coords = tuple(int(x) for x in rng.integers(0, 10, size=(2)))
    #makes a random x and y value and stores it as a tuple
    print(f"Your opponent is attacking {coords}")
    #returns the coodinates
    return coords

def ai_opponent_game_loop():
    #a game loop where the player attacks then the ai attacks until someone wins
    print("welcome to the game")

    player_board = comp.place_battleships(comp.initialise_board(), comp.read_placement(), 'custom')
    #creates the players board with the placement.json file
    
    opponent_board = comp.place_battleships(comp.initialise_board(), comp.create_battleships(), 'random')
    #creates a random board for the opponent

    player_health = comp.create_battleships()
    #creates the players health
    opponent_health = comp.create_battleships()
    #creates the opponents health

    players.update({"player": {"Board": player_board, "Health": player_health}, "opponent": {"Board": opponent_board, "Health": opponent_health}})
    #adds the player and opponents health and boards to a dictionary
    #to store game information neatly
    
    while sum(players["player"]["Health"].values()) != 0 and sum(players["opponent"]["Health"].values()) != 0:
        #while neither players health is 0 the game continues
        
        print("your turn")
        gm.attack(gm.cli_coordinates_input(), players["opponent"]["Board"], players["opponent"]["Health"])
        #player attacks and can input coordinates and hits the opponents board

        print("opponents turn")
        gm.attack(generate_attack(), players["player"]["Board"], players["player"]["Health"])
        #opponent attacks with random coordinates on the player board

        for i in players["player"]["Board"]:
            #creates an ascii representation of the board
            for j in i:
                if j != None:
                    print(j[0], end = " ")
                else:
                    print("O", end = " ")
            print()

    if sum(players["opponent"]["Health"].values()) == 0:
        #when while loop ends checks whos health is 0 to determine winner, if its a draw the user wins as they went first
        print("You WON!!!")
    else:
        print("Your Opponent Won :(")

if __name__ == '__main__':
    ai_opponent_game_loop()

