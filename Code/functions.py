#imports
import random
import classes as cla

#functions

#roll dice
def dice():
    a = random.randint(1,6)
    b = random.randint(1,6)
    return a + b

#buy the space the player landed on
def buy(player, space, cost):
    player.money -= cost
    player.props.append(space)

#player pays another player a certain amount
def pay(player1, player2, amount):
    player1.money -= amount
    player2.money += amount

#returns player that owns a space of given id
def owner(players, id) -> cla.Player:
    for player in players:
        if id in player.props:
            return player
        
