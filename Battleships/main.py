from flask import Flask, render_template, request, jsonify
import components as comp
import game_engine as gm
from mp_game_engine import generate_attack
import json


app = Flask(__name__)
#initialises app

players = {}
#empty players dictionary to store player and opponent health and boards

opponent_board = comp.place_battleships(comp.initialise_board(), comp.create_battleships(), 'random')
#creates the opponents board

player_health = comp.create_battleships()
opponent_health = comp.create_battleships()
#gives both players their health

@app.route('/placement', methods = ['POST', 'GET'])
def placement_interface():
    #initialises the placement webpage
    if request.method == 'GET':
        #when visited it inputs a dictionary for
        #the webpage to use to know what kind of ships to place
        ships = comp.create_battleships()
        return render_template('placement.html', ships = ships, board_size = 10)
    
    if request.method == 'POST':
        #when the button is pressed to send the ships placed back to main
        data = request.get_json()
        #data is a dictionary of the starting coordinates of the ships
        #and the orientation of the ship
        with open('placement.json', 'w') as json_file:
            #opens the placement.json file and replaces it with the new placed ships
            json.dump(data, json_file, indent=2)
        #sends a message to the user to let them know it worked
        return jsonify({'message': 'Received'}), 200


@app.route('/', methods = ['GET'])
def root():
    #the main webpage with your board and where you have attacked visible
    player_board = comp.place_battleships(comp.initialise_board(), comp.read_placement(), 'custom')
    #creates the players board out of the placement.json file
    players.update({"player": {"Board": player_board, "Health": player_health}, "opponent": {"Board": opponent_board, "Health": opponent_health}})
    #creates a dictionary to store all the game information neatly
    if request.method == 'GET':
        #sends the players board to the webpage
        return render_template('main.html', player_board = player_board)
    
@app.route('/attack', methods = ['GET'])
def process_attack():
    #creates a method to do 1 loop through the games whole loop
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    #gets coordinates from what grid the user presses
    coordinates = (x,y)

    hit = gm.attack(coordinates, players["opponent"]["Board"], players["opponent"]["Health"])
    #both attacks the tile hit and returns whether it is hit or not as boolean values
    ai_turn = generate_attack()
    #creates an attack for the ai to do to user
    gm.attack(ai_turn, players['player']['Board'], players['player']['Health'])
    #performs the attack on the players board

    if sum(players["player"]["Health"].values()) == 0:
        #if the players health reaches 0 the player lose and the game ends
        game_finished = True
        #finishes the game when the next loop ends
        finished = 'Your Opponent wins :('

    elif sum(players["opponent"]["Health"].values()) == 0:
        #if the opponents health reaches 0 the player wins and the game ends
        game_finished = True
        #finishes the game when the next loop ends
        finished = 'Your Win Congratulations :)'
    else:
        game_finished = False
    
    if game_finished == False:
        #repeats game loop if the game isnt finished
        return jsonify({'hit': hit,
            'AI_Turn': ai_turn
            })
    else:
        #does a final game loop before ending the game
        return jsonify({'hit': hit,
            'AI_Turn': ai_turn,
            'finished': finished
            })

if __name__ == '__main__':
    app.run()


