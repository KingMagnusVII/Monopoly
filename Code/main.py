#ACTUAL MAIN FILE 
import tkinter as tk
import GUI as mg
import classes as cla
from functools import partial
import random
import functions as fx
import GUIfxn as gfx
import pandas as pd
import DataArrays
import PATH

final=gfx.runmenu()
PATH= PATH.path #path file addition

properties = pd.read_csv(PATH + "Data-Files/properties.csv", index_col=0)
railroads = pd.read_csv(PATH + "Data-Files/railroads.csv", index_col = 0)
sproperties = pd.read_csv(PATH + "Data-Files/sproperties.csv", index_col=0)

key = {'P' : properties, 'RR' : railroads, 'U' : sproperties} #internal reference codes

class GameLoop:

    def __init__(self, root): #initialization

        global final
        self.rootf=root

        self.turn=-1 #to start at 0 when turnchange() is called

        if(final[0]=="S"):
            self.loadfile(final[1])
        else:
            self.root= mg.GameGUI(self.rootf, final) #placeholder window
            self.players=self.root.player

        self.root.root.protocol("WM_DELETE_WINDOW", self.rusure)
        self.numpl=len(final) #no.of players

        self.root.roll.config(command=partial(self.OnDiceRoll, [self.turn+1, random.randint(1,6),random.randint(1,6), self.players[self.turn+1].space] )) #initialization of the first roll

        self.props=['Go','MEDITERRANEAN AVENUE', 'Com', 'BALTIC AVENUE', 'Tax', 'READING RAILROAD', 'ORIENTAL AVENUE', 'Ch', 'VERMONT AVENUE', 'CONNECTICUT AVENUE', 'Jail',
       'ST. CHARLES PLACE', 'ELECTRIC COMPANY', 'STATES AVENUE', 'VIRGINIA AVENUE', 'PENNSYLVANIA RAILROAD', 'ST. JAMES PLACE', 'Com', 
       'TENNESSEE AVENUE', 'NEW YORK AVENUE', 'FP', 'KENTUCKY AVENUE', 'Ch', 'INDIANA AVENUE', 'ILLINOIS AVENUE', 'B. & O. RAILROAD', 
       'ATLANTIC AVENUE', 'VENTNOR AVENUE', 'WATER WORKS', 'MARVIN GARDENS', 'GTJ', 'PACIFIC AVENUE', 'NORTH CAROLINA AVENUE', 'Com', 
       'PENNSYLVANIA AVENUE', 'SHORT LINE RAILROAD', 'Ch', 'PARK PLACE', 'Tax', 'BOARDWALK']
            
    def OnDiceRoll(self, rolllist): #execute when roll button is pressed
        
        
        if(self.players[self.turn].isJailed>-1): #is being jailed condition
            pass
        else:
            self.root.diceroll(rolllist) #function for moving icon
            self.players[self.turn].space = (self.players[self.turn].space + rolllist[1] + rolllist[2] ) %40 #space updation
        
        #TILE EVENTS - independent of player
        #pass go
        if self.players[self.turn].space < (rolllist[1] + rolllist[2]):
            self.players[self.turn].money += 200
            self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
        
        #update roll list for next dice roll    
        global realRoll
        realRoll = tuple(rolllist)
        rolllist=[(self.turn+1)%self.numpl, random.randint(1,6),random.randint(1,6), self.players[(self.turn+1)%self.numpl].space] #gives a new list of random values and assigns it to the roll btn
        self.root.roll.config(command = partial( self.OnDiceRoll, rolllist)) 
        
        #TILE ACTIONS
        if(self.players[self.turn].money<=0): #bankruptcy
            self.players[self.turn].props=[]
            self.pop_up("turn skipped.")
        
        elif(self.players[self.turn].isJailed>-1): #is being jailed condition
            self.players[self.turn].isJailed-=1
            self.pop_up(self.players[self.turn].name+ "'s turn has been skipped for being jailed.")

        #buy mechanism
        elif (fx.owner(self.players, self.props[self.players[self.turn].space]) == None and self.props[self.players[self.turn].space] not in ["Com", "Ch", "GTJ", "FP", "Go", "Tax", "Jail"]): #unowned condition
            
            if ('RAILROAD' in self.props[self.players[self.turn].space].split()): #checks if 'RAILROAD' is in the name
                self.root.buy.config(state="normal", command=partial(self.buying, self.props[self.players[self.turn].space], 'RR')) #railway buy button
            elif (self.props[self.players[self.turn].space] in ['WATER WORKS', 'ELECTRIC COMPANY']):
                self.root.buy.config(state="normal", command=partial(self.buying, self.props[self.players[self.turn].space], 'U'))
                #utility buy button
            else:
                self.root.buy.config(state="normal", command=partial(self.buying, self.props[self.players[self.turn].space], 'P')) #function for buy btn
            self.root.notbuy.config(state="normal", command=partial(self.passing) ) #function for pass btn

        elif (fx.owner(self.players, self.props[self.players[self.turn].space])==self.players[self.turn]): #checks if the guy owns his own property to not softlocks
            self.turnchange()

        #rent mechanism
        elif (fx.owner(self.players, self.props[self.players[self.turn].space]) != None and fx.owner(self.players, self.props[self.players[self.turn].space]) != self.players[self.turn]):
            if ('RAILROAD' in self.props[self.players[self.turn].space].split()): #checks if 'RAILROAD' is in the name
                self.paying('RR')
            elif (self.props[self.players[self.turn].space] in ['WATER WORKS', 'ELECTRIC COMPANY']):
                self.paying('U')
            else:
                self.paying('P')
            
        elif (self.props[self.players[self.turn].space] in ['Ch','Com']): #Chance/Community Chest
            self.Chance_Community_Gamble()
        
        elif (self.props[self.players[self.turn].space] == 'Tax'): #Income Tax
            
            self.root.moneycountdown(self.players[self.turn].money-200,self.players[self.turn].money, 0)
            self.players[self.turn].money -= 200
            self.pop_up(self.players[self.turn].name+" paid Income Tax of 200. Good work citizen.")


        elif (self.props[self.players[self.turn].space] == 'GTJ'): #Go to Jail
            self.root.optimus(self.turn, self.players[self.turn].space, (50-self.players[self.turn].space))
            self.players[self.turn].space=10
            self.pop_up(self.players[self.turn].name+" is jailed.")
            self.escape_jail(self.players[self.turn])
        
        elif (self.props[self.players[self.turn].space] in ["FP", "Go", "Jail"]): #Free Parking/Go/Jail - do nothing
            self.turnchange()
               
    def buying(self, property, code):
        
        propArrayKey = {'P' : self.players[self.turn].props, 'RR' : self.players[self.turn].railroad, 'U' : self.players[self.turn].sprop}
        
        self.root.moneycountdown(self.players[self.turn].money-key[code].at[self.props[self.players[self.turn].space], 'price'], self.players[self.turn].money, 0)
        self.players[self.turn].money-=key[code].at[self.props[self.players[self.turn].space], 'price']
        self.players[self.turn].props.append(property)
        if (code != 'P'):
            propArrayKey[code].append(property)
        self.root.buy.config(state="disabled")     #disabling btns after the buy function is done
        self.root.notbuy.config(state="disabled")
        self.pop_up("Property "+self.props[self.players[self.turn].space]+" has been bought by "+self.players[self.turn].name)

    def passing(self): #not buying

        self.root.buy.config(state="disabled")     
        self.root.notbuy.config(state="disabled")    #literally does nothing - disables buttons
        self.turnchange()

    def paying(self, code): #paying rent
        
        mod = {'P' : 1, 'RR' : 2**(len(fx.owner(self.players, self.props[self.players[self.turn].space]).railroad)-1), 'U' : (realRoll[1] + realRoll[2]) * (6*len(fx.owner(self.players, self.props[self.players[self.turn].space]).sprop) - 2)}  #1-2 maps to 4-10 with 6x-2
        
        fx.pay(self.players[self.turn], fx.owner(self.players, self.props[self.players[self.turn].space]), key[code].at[self.props[self.players[self.turn].space], 'rent'] * mod[code])
        self.root.moneycountdown(self.players[self.turn].money, fx.owner(self.players, self.props[self.players[self.turn].space]).money+key[code].at[self.props[self.players[self.turn].space], 'rent'] * mod[code], 0)
        self.pop_up(self.players[self.turn].name+" paid amount "+str(key[code].at[self.props[self.players[self.turn].space], 'rent'] * mod[code])+" to "+fx.owner(self.players, self.props[self.players[self.turn].space]).name)

    def turnchange(self):
        self.root.moneycountdown(self.players[(self.turn+1)%self.numpl].money, self.players[self.turn].money, 0)
        self.turn=(self.turn+1)%self.numpl
        self.root.blink(self.players[self.turn].color, 3, 0)
        self.root.ui_plinfo(self.players[self.turn].name) #updates playerinfo to next player
        self.root.ui_bal(self.players[self.turn].money) #updates money
        self.root.ui_owned(self.players, self.players[self.turn].props) #updates owned properties
        self.root.playgif() #plays the gif

    def pop_up(self, s):

        flower=tk.Tk()
        flower.config(bg="black")
        flower.title("USER INFO")
        message=tk.Label(flower, text=s, bg="black", fg="white", font=("Times New Roman", 18))
        message.pack(padx=50, pady=20)

        def on_close():
            flower.destroy()
            self.turnchange()
        #flower.protocol("WM_DELETE_WINDOW", on_close)
        flower.after(2000, on_close)

        flower.mainloop()

    def ChanceRandomizer(self):
        self.chance_Statement = DataArrays.chance
        self.chance_Image = DataArrays.chance_image
        self.chance_amount = DataArrays.chance_amount
        self.random_choice = random.randint(0, len(self.chance_Statement) - 1)
        self.players[self.turn].money += self.chance_amount[self.random_choice]

        self.root.chancom(self.chance_Image[self.random_choice]) #image of card call
        self.root.ch.config(command=lambda: None) #removing function of button

        #Get out of jail card and Go to Jail actions
        if(self.chance_Statement[self.random_choice] == 'Get Out of Jail Free - This card may be kept until needed or sold'):
            self.players[self.turn].getoutofjailcard += 1
            self.turnchange()
        
        if(self.chance_Statement[self.random_choice] == 'Go directly to Jail - Do not pass Go, do not collect $200'):
            self.root.optimus(self.turn, self.players[self.turn].space, (50-self.players[self.turn].space))
            self.players[self.turn].space = 10
            self.escape_jail(self.players[self.turn])
            self.turnchange()
        
        if(self.chance_Statement[self.random_choice] == 'Advance to Go (Collect $200)'):
            self.root.optimus(self.turn, self.players[self.turn].space, (40-self.players[self.turn].space))
            self.players[self.turn].space = 0
            self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
            self.players[self.turn].money += 200
            self.turnchange()
        
        if(self.chance_Statement[self.random_choice] == 'Advance to Illinois Ave.'):
            self.root.optimus(self.turn, self.players[self.turn].space, (64-self.players[self.turn].space))
            self.players[self.turn].space = 24
            if(self.players[self.turn].space < (realRoll[1] + realRoll[2])):
                self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
                self.players[self.turn].money += 200
            self.OnDiceRoll([self.turn, 0, 0, self.players[self.turn].space])
               
        if(self.chance_Statement[self.random_choice] == 'Advance to St. Charles Place'):
            self.root.optimus(self.turn, self.players[self.turn].space,  (51-self.players[self.turn].space))
            self.players[self.turn].space = 11
            if(self.players[self.turn].space < (realRoll[1] + realRoll[2])):
                self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
                self.players[self.turn].money += 200
            self.OnDiceRoll([self.turn, 0, 0, self.players[self.turn].space])
            
        if(self.chance_Statement[self.random_choice] == 'Bank pays you dividend of $50'):
            self.root.moneycountdown(self.players[self.turn].money+50,self.players[self.turn].money, 0)
            self.players[self.turn].money += 50
            self.turnchange()
        
        if(self.chance_Statement[self.random_choice] == 'Go Back 3 Spaces'):
            self.root.optimus(self.turn, self.players[self.turn].space, 37)
            self.players[self.turn].space = (self.players[self.turn].space + 37) % 40
            self.OnDiceRoll([self.turn, 0, 0, self.players[self.turn].space])
        
        if(self.chance_Statement[self.random_choice] == 'Pay poor tax of $15'):
            self.root.moneycountdown(self.players[self.turn].money-15,self.players[self.turn].money, 0)
            self.players[self.turn].money -= 15
            self.pop_up(self.players[self.turn].name+" paid a poor tax of 15. Good work citizen.")
        
        if(self.chance_Statement[self.random_choice] == 'Take a trip to Reading Railroad'):
            self.root.optimus(self.turn, self.players[self.turn].space, (45-self.players[self.turn].space))
            self.players[self.turn].space = 5
            if(self.players[self.turn].space < (realRoll[1] + realRoll[2])):
                self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
                self.players[self.turn].money += 200
            self.OnDiceRoll([self.turn, 0, 0, self.players[self.turn].space])
        
        if(self.chance_Statement[self.random_choice] == 'Advance to Boardwalk'):
            self.root.optimus(self.turn, self.players[self.turn].space, (39-self.players[self.turn].space))
            self.players[self.turn].space = 39
            self.OnDiceRoll([self.turn, 0, 0, self.players[self.turn].space])
               
        if(self.chance_Statement[self.random_choice] == 'You have been elected Chairman of the Board - Pay each player $50'):
            for player in self.players:
                if player != self.players[self.turn]:
                    fx.pay(self.players[self.turn], player, 50)
            self.root.moneycountdown(self.players[self.turn].money-(50*self.numpl),self.players[self.turn].money, 0)
            self.pop_up(self.players[self.turn].name+" has been elected Chairman of the Board and paid each player $50.")
        
        if(self.chance_Statement[self.random_choice] == 'Your building loan matures - Collect $150'):
            self.root.moneycountdown(self.players[self.turn].money+150,self.players[self.turn].money, 0)
            self.players[self.turn].money += 150
            self.turnchange()
        
    def CommunityRandomizer(self):
        self.community_Statement = DataArrays.community
        self.community_Image = DataArrays.community_image
        self.community_amount = DataArrays.community_amount
        self.random_choice = random.randint(0, len(self.community_Statement) - 1)
        self.players[self.turn].money += self.community_amount[self.random_choice]

        self.root.chancom(self.community_Image[self.random_choice])
        self.root.cc.config(command=lambda: None)

        #Get out of jail card and Go to Jail actions
        if(self.community_Statement[self.random_choice] == 'Get Out of Jail Free - This card may be kept until needed or sold'):
            self.players[self.turn].getoutofjailcard += 1
            
        
        if(self.community_Statement[self.random_choice] == 'Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200'):
            self.root.optimus(self.turn, self.players[self.turn].space, (50-self.players[self.turn].space))
            self.players[self.turn].space=10
            self.escape_jail(self.players[self.turn])

        if(self.community_Statement[self.random_choice] == 'Advance to Go (Collect $200)'):
            self.root.optimus(self.turn, self.players[self.turn].space, (40-self.players[self.turn].space))
            self.players[self.turn].space = 0
            self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
            self.players[self.turn].money += 200

        if(self.community_Statement[self.random_choice] == 'Bank error in your favor - Collect $200'):
            self.root.moneycountdown(self.players[self.turn].money+200,self.players[self.turn].money, 0)
            self.players[self.turn].money += 200

        if(self.community_Statement[self.random_choice] == 'Doctor\'s fees - Pay $50'):
            self.root.moneycountdown(self.players[self.turn].money-50,self.players[self.turn].money, 0)
            self.players[self.turn].money -= 50
            
        if(self.community_Statement[self.random_choice] == 'From sale of stock you get $50'):
            self.root.moneycountdown(self.players[self.turn].money+50,self.players[self.turn].money, 0)
            self.players[self.turn].money += 50 

        if(self.community_Statement[self.random_choice] == 'Grand Opera Night - Collect $50 from every player'):
            for player in self.players:
                if player != self.players[self.turn]:
                    fx.pay(player, self.players[self.turn], 50)
                    self.root.moneycountdown(player.money + (50*self.numpl), self.players[self.turn].money, 0)
            self.pop_up(self.players[self.turn].name+" has collected $50 from every player for Grand Opera Night.")

        if(self.community_Statement[self.random_choice] == 'Holiday Fund matures - Collect $100'):
            self.root.moneycountdown(self.players[self.turn].money+100,self.players[self.turn].money, 0)
            self.players[self.turn].money += 100
        
        if(self.community_Statement[self.random_choice] == 'Income tax refund - Collect $20'):
            self.root.moneycountdown(self.players[self.turn].money+20,self.players[self.turn].money, 0)
            self.players[self.turn].money += 20
        
        if(self.community_Statement[self.random_choice] == 'Life insurance matures - Collect $100'):
            self.root.moneycountdown(self.players[self.turn].money+100,self.players[self.turn].money, 0)
            self.players[self.turn].money += 100

        if(self.community_Statement[self.random_choice] == 'Pay hospital fees of $100'):
            self.root.moneycountdown(self.players[self.turn].money-100,self.players[self.turn].money, 0)
            self.players[self.turn].money -= 100
        
        if(self.community_Statement[self.random_choice] == 'Pay school fees of $150'):
            self.root.moneycountdown(self.players[self.turn].money-150,self.players[self.turn].money, 0)
            self.players[self.turn].money -= 150

        if(self.community_Statement[self.random_choice] == 'You have won second prize in a beauty contest - Collect $10'):
            self.root.moneycountdown(self.players[self.turn].money+10,self.players[self.turn].money, 0)
            self.players[self.turn].money += 10

        if(self.community_Statement[self.random_choice] == 'You inherit $100'):
            self.root.moneycountdown(self.players[self.turn].money+100,self.players[self.turn].money, 0)
            self.players[self.turn].money += 100

        if(self.community_Statement[self.random_choice] == 'From sale of stock you get $45'):
            self.root.moneycountdown(self.players[self.turn].money+45,self.players[self.turn].money, 0)
            self.players[self.turn].money += 45

        self.turnchange()
        
    def Chance_Community_Gamble(self):
        if self.props[self.players[self.turn].space] == 'Ch':
            self.root.ch.config(state='active')
            self.root.ch.config(command=partial(self.ChanceRandomizer) )

        elif self.props[self.players[self.turn].space] == 'Com':
            self.root.cc.config(state='active')
            self.root.cc.config(command=partial(self.CommunityRandomizer) ) 
            
    def jail(self, player): #jailing mechanism
        print(player.name + "is jailed lmao")
        player.isJailed = 2  # Set jailed status
        #player.money -= 200  # Deduct $200 for going to jail

    def escape_jail(self, player): #get out of jail mechanism

        if player.getoutofjailcard > 0:
            player.getoutofjailcard -= 1
            player.isJailed = -1 #default value
            
        else:
            self.jail(player)

        # elif player.money >= 50:
        #     player.money -= 50
        #     player.isJailed = -1
        #     player.space = 10
    
    def rusure(self): #do u wish save pop up

        term=tk.Toplevel()
        term.geometry("450x200")
        term.resizable(False,False)
        term.title("Reconsideration required")
        term.config(bg="black")

        lb=tk.Label(term, text="Are you sure you wish to exit without saving?\nIf you wish to save, ensure the turn is finished.", font=("Times New Roman", 15), bg="black", fg="white", width=40)
        lb.pack(padx=20, pady=(20,10))

        btnf=tk.Frame(term, bg="black")
        btnf.pack(anchor="center", pady=20)

        def filenamesave(): #function to make pop ups to get filename and savefiles
    
            self.name="" #name of savefile
            root=tk.Tk()
            root.title("Name your file")
            root.resizable(False,False)
            root.config(bg="black")
            root.geometry("320x180")

            f=tk.Frame(root,bg="black", highlightcolor="white", highlightthickness=3) #frame
            f.pack(fill="both", expand=True, padx=10, pady=10)

            lb=tk.Label(f, text="Enter name of Save File", font=("Times New Roman", 18), bg="black", fg="white") #label 
            lb.pack(padx=10, pady=(10,5), anchor="center")

            ne=tk.Entry(f, width=20, font=("Times New Roman", 18), bg="black", fg="white", insertbackground="white") #name entry box
            ne.pack(padx=10,pady=(0,10), anchor="center")

            def taketh(): # function to get the name entry from entrybox and do the saving
                
                self.name=ne.get()

                def save(savename): #function to save a file
                    file = open(PATH + 'saves/' + savename + '.txt', 'w')
                    file.write(str(final) + '\n')
                    file.write(str(self.turn) + '\n')
                    for i in self.players:
                        file.write(str(i.name) + ':')
                        file.write(str(i.color) + ':')
                        file.write(str(i.props) + ':')
                        file.write(str(i.sprop) + ':')
                        file.write(str(i.railroad) + ':')
                        file.write(str(i.getoutofjailcard) + ':')
                        file.write(str(i.money) + ':')
                        file.write(str(i.space) + ':')
                        file.write(str(i.isJailed) + ':')
                        file.write('\n')
                    file.close()

                save(self.name)

                term.destroy() #destroy all windows
                self.root.root.destroy()
                root.destroy()

            con=tk.Button(f, text="Confirm", font=("Times New Roman", 18), bg="black", fg="white", command=taketh) #confirm button
            con.pack(padx=10, pady=5, anchor="center")

            root.mainloop()
 
        btn1=tk.Button(btnf, text="Save", font=("Times New Roman", 15), bg="black", fg="white", width=14, command=filenamesave) #Save button
        btn1.pack(side="left", padx=(10,20), pady=0)
        btn2=tk.Button(btnf, text="Do not Save", font=("Times New Roman", 15), bg="black", fg="white", width=14, command=self.root.root.destroy) #Do not Save button
        btn2.pack(side="right", padx=(10,20), pady=0)

        term.mainloop()
            
    def loadfile(self, savename):
        file = open(PATH + 'saves/' + savename, 'r')
        data = file.readlines()

        global final 
        final = eval(data[0])
        self.root= mg.GameGUI(self.rootf, final) #placeholder window
        self.players=self.root.player
        self.turn = int(data[1][0])-1
        
        counter=0 
        for i in self.players: #loading data into player object
            line = data[2+counter].split(':')
            i.props = eval(line[2])
            i.sprop = eval(line[3])
            i.railroad = eval(line[4])
            i.getoutofjailcard = int(line[5])
            i.money = int(line[6])
            i.space = int(line[7])
            self.root.carl[counter].place(x=self.root.loc[i.space][0]+self.root.cor[counter][0],y=self.root.loc[i.space][1]+self.root.cor[counter][1])
            i.isJailed = int(line[8])
            counter+=1
        file.close()
        
def run_game():
    root = tk.Tk()
    game = GameLoop(root)
    game.turnchange()
    root.mainloop()

run_game()
