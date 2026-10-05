#player class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.props = []  #properties owned by player
        self.sprop = [] #special properties owned by player
        self.railroad = [] #railroads owned by user
        self.getoutofjailcard = 0
        self.money = 1500
        self.space = 0
        self.isJailed = -1  #number of turns player has been jailed for
