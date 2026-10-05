import tkinter as tk
import GUIfxn                       
from functools import partial       #to preload a function without calling it
from PIL import Image, ImageTk      #to resize images
import random
import classes as cla
import functions as fx
import pandas as pd
import PATH

PATH= PATH.path #path file addition

properties = pd.read_csv(PATH + "Data-Files/properties.csv", index_col=0)

class GameGUI:
    
    def __init__(self, root, final): #board design

        self.root=root
        self.root.title("Monopoly")
        self.root.geometry("900x846")    #window creation
        self.root.config(bg="black")
        self.root.resizable(False, False)

        self.bd=tk.Frame(root,bg="lightblue", borderwidth="2", relief="solid") #Main Board Frame: Grid system
        self.bd.pack(padx=100, pady=(10,190), side="top", fill="x")
        self.bd.pack_propagate(False) #prevent resizing of board due to random stuff

        for i in range (0,11):      #main board frame, columns and rows initialization, self.bd-frame, its a grid system so u make col and rows
            self.bd.columnconfigure(i, weight=1)
            self.bd.rowconfigure(i, weight=1)

        #variable initialisation
        self.player=[]
        for i in range(len(final)): #loading in the players
            self.player.append(cla.Player(final[i][0],final[i][1]))
        #self.player= [cla.Player("ZEUS", "lightgrey"), cla.Player("POSEIDON", "blue"), cla.Player("HADES", "grey"), cla.Player("KRONOS", "red")] #player here is different from players in gameloop but has same value for desgin purposes
        bt=[['' for i in range(11)] for j in range (11) ] #button/property, every button on the board has function and has an image on it
        pain=[['' for i in range(11) ] for j in range (11) ] #frame on the board: it divides one title into a button and a strip(color)
        strip=[['' for i in range(11) ] for j in range (11) ] #color strip next to a button
        col=[["" for i in range(4) ] for j in range (11) ] #colours storage
        prop=[["" for i in range(11) ] for j in range (11) ] #property name storage
        self.img=[""]
        self.house={} #house info

        #colours
        col[0]=["","orange","orange","white","orange","white","pink","pink","white","pink"]
        col[1]=["","red","white","red","red","white","yellow","yellow","white","yellow"]
        col[2]=["","lightblue","lightblue","white","lightblue","white","white","brown","white","brown"]
        col[3]=["","green","green","white","green","white","white","blue","white","blue"]

        #properties
        prop[0]=["","NEW YORK AVENUE","TENNESSEE AVENUE","","ST. JAMES PLACE","PENNSYLVANIA RAILROAD","VIRGINIA AVENUE","STATES AVENUE","ELECTRIC COMPANY","ST. CHARLES PLACE"]
        prop[1]=["","KENTUCKY AVENUE","","INDIANA AVENUE","ILLINOIS AVENUE","B. & O. RAILROAD","ATLANTIC AVENUE","VENTNOR AVENUE","WATER WORKS","MARVIN GARDENS"]
        prop[2]=["","CONNECTICUT AVENUE","VERMONT AVENUE","","ORIENTAL AVENUE","READING RAILROAD","","BALTIC AVENUE","","MEDITERRANEAN AVENUE"]
        prop[3]=["","PACIFIC AVENUE","NORTH CAROLINA AVENUE","","PENNSYLVANIA AVENUE","SHORT LINE RAILROAD","","PARK PLACE","","BOARDWALK"]

        for i in range (1,89):      #image initializing, assigning all images to array to prevent garbage collection
            
            if(i<54 or i>59):
                proimg=Image.open(PATH + f"Images\\image{i}.png" )

            if(i in [2,4,5,7,20,23,26]):                                #horizontal rows blanks like chance and electrical
                proimg=proimg.resize((65,85), Image.Resampling.LANCZOS) #resizing images
                self.img.append(ImageTk.PhotoImage(proimg))  #giving image to list and converting image to tkinter format
                continue
            elif(i in [11,14,16,30,32,33,35]):                          #vertical cloumns blanks
                proimg=proimg.resize((80,55), Image.Resampling.LANCZOS)
                self.img.append(ImageTk.PhotoImage(proimg))
                continue
            elif((i>=1 and i<=9) or (i>=19 and i<=27)):                  #horizontal properties
                proimg=proimg.resize((55,60), Image.Resampling.LANCZOS)
            elif((i>=10 and i<=18) or (i>=28 and i<=36)):                #vertical properties
                proimg=proimg.resize((65,50), Image.Resampling.LANCZOS)
            elif(i>=36 and i<=40):                                       #corners
                proimg=proimg.resize((85,76), Image.Resampling.LANCZOS)
            elif(i>=41 and i<=44):                                       #player pieces
                proimg=proimg.resize((20,20), Image.Resampling.LANCZOS) 
            elif(i==45):                                                 #center piece
                proimg=proimg.resize((528,485), Image.Resampling.LANCZOS) 
            elif(i==46 or i==47):
                proimg=proimg.resize((150,110), Image.Resampling.LANCZOS) #chance and community chest
                proimg = proimg.rotate(45, expand="true") 
            elif(i>=48 and i<=53):                                        #dice imgage
                proimg=proimg.resize((50,50), Image.Resampling.LANCZOS)
            elif(i>=54 and i<=59):                                        #default dummy pictures
                proimg=Image.open(PATH+ f"Images\\image45.png" )
                proimg=proimg.resize((528,485), Image.Resampling.LANCZOS)
            elif(i>=60 and i<=86):                                        #chance 75-86 and community chest 60-74
                proimg=proimg.resize((295,171), Image.Resampling.LANCZOS) 
            elif(i in [87,88]):                                           #houses and hotel
                proimg=proimg.resize((10,10), Image.Resampling.LANCZOS) 

            self.img.append(ImageTk.PhotoImage(proimg))

        for i in range(0,11):      #buttons/properties, giving them design, function and location
                                #5 sections- left, right, top, bottom, corners (5 types of design)

            for j in range(0,11):   # i- column, j - rows

                if( i==0 and (j!=0 and j!=10) ): #left column button/property
                                                                            
                    if (j in [3,5,8] ):      #vertical blanks have a different secction cuz they dont need a strip

                                        #button creation with a function on press gives a pop up
                        bt[j][i]=tk.Button(self.bd, text="", height="4", width="11", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[0][j], col[0][j]) )
                        bt[j][i].grid(row=j, column=i, padx=1, pady=1, sticky="news")      #location of button in self.bd
                        bt[j][i].config(image=self.img[19-j], anchor="center", height="135", width="90")      #updating the button with the image
                        continue

                    pain[j][i]=tk.Frame(self.bd, height="4", width="11")      #buttons with strip, the above had no strips, pain-frame for grid
                    pain[j][i].grid(row=j, column=i, sticky="news")      #location of pain in self.bd
                    pain[j][i].columnconfigure(0, weight=1)     #making 2 columns, 2nd column is strip and 1st column is button in this case
                    pain[j][i].columnconfigure(1, weight=1)
                    pain[j][i].rowconfigure(0, weight=1)    #has one row obv

                    #button creation with function again
                    bt[j][i]=tk.Button(pain[j][i], text="", height="4", width="7", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[0][j], col[0][j]) )
                    bt[j][i].grid(row=0, column=0, padx=1, pady=1, sticky="news")   #location of button in pain (not self.bd cuz we made a new frame for the strip and the button)
                    bt[j][i].config(image=self.img[(19-j)], anchor="center", height="135", width="90")   #updating button with image, (19-j) for image


                    strip[j][i]=tk.Label(pain[j][i], text="", height="4", width="4", bg=col[0][j], font=("Times New Roman",15) ) #making a coloured strip
                    strip[j][i].grid(row=0, column=1, padx=1, pady=1, sticky="news") #location of strip in pain
                
                #this same code structure is repeated 3 other times with changes in design and numbers
                
                elif( i==10 and (j!=0 and j!=10) ): #right column button/property

                    if (j in [3,5,6,8]):
                        bt[j][i]=tk.Button(self.bd, text="", height="4", width="11", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[3][j], col[3][j])  )
                        bt[j][i].grid(row=j, column=i, padx=1, pady=1, sticky="news")
                        bt[j][i].config(image=self.img[27+j], anchor="center", height="135", width="90")
                        continue
                    
                    pain[j][i]=tk.Frame(self.bd, height="4", width="11")
                    pain[j][i].grid(row=j, column=i, sticky="news")
                    pain[j][i].columnconfigure(0, weight=1)
                    pain[j][i].columnconfigure(1, weight=1)
                    pain[j][i].rowconfigure(0, weight=1)

                    bt[j][i]=tk.Button(pain[j][i], text="", height="4", width="7", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[3][j], col[3][j]) )
                    bt[j][i].grid(row=0, column=1, padx=1, pady=1, sticky="news")
                    bt[j][i].config(image=self.img[27+j], anchor="center", height="135", width="90") # (27+j) for image

                    strip[j][i]=tk.Label(pain[j][i], text="", height="4", width="4", bg=col[3][j], font=("Times New Roman",15) )
                    strip[j][i].grid(row=0, column=0, padx=1, pady=1, sticky="news")


                elif( (i>0 and i<10) and j==0 ): #top row button/property

                    if(i in [2,5,8] ):
                        bt[j][i]=tk.Button(self.bd, text="", height="5", width="9", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[1][i], col[1][i]) )
                        bt[j][i].grid(row=j, column=i, padx=1, pady=1, sticky="news")
                        bt[j][i].config(image=self.img[18+i], anchor="center", height="100", width="120")
                        continue

                    pain[j][i]=tk.Frame(self.bd, height="5", width="9")
                    pain[j][i].grid(row=j, column=i, sticky="news")
                    pain[j][i].columnconfigure(0, weight=1)
                    pain[j][i].rowconfigure(0, weight=1)
                    pain[j][i].rowconfigure(1, weight=1)
                    
                    bt[j][i]=tk.Button(pain[j][i], text="", height="3", width="9", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[1][i], col[1][i]) )
                    bt[j][i].grid(row=0, column=0, padx=1, pady=1, sticky="news")
                    bt[j][i].config(image=self.img[18+i], anchor="center", height="100", width="95") # (18+i) for image

                    strip[j][i]=tk.Label(pain[j][i], text="", height="2", width="9", bg=col[1][i], font=("Times New Roman",18) )
                    strip[j][i].grid(row=1, column=0, padx=1, pady=1, sticky="news")


                elif( (i>0 and i<10) and j==10 ): #bottom row button/property

                    if(i in [3,5,6,8] ):
                        bt[j][i]=tk.Button(self.bd, text="", height="5", width="9", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[2][i],col[2][i]) )
                        bt[j][i].grid(row=j, column=i, padx=1, pady=1, sticky="news")
                        bt[j][i].config(image=self.img[(10-i)], anchor="center", height="100", width="120")
                        continue

                    pain[j][i]=tk.Frame(self.bd, height="5", width="9")
                    pain[j][i].grid(row=j, column=i, sticky="news")
                    pain[j][i].columnconfigure(0, weight=1)
                    pain[j][i].rowconfigure(0, weight=1)
                    pain[j][i].rowconfigure(1, weight=1)

                    bt[j][i]=tk.Button(pain[j][i], text="", height="3", width="9", font=("Times New Roman",18), command=partial(GUIfxn.msg, self.player, prop[2][i],col[2][i]) )
                    bt[j][i].grid(row=1, column=0, padx=1, pady=1, sticky="news")
                    bt[j][i].config(image=self.img[(10-i)], anchor="center", height="100", width="95") # (10-i) for image

                    strip[j][i]=tk.Label(pain[j][i], text="", height="2", width="9", bg=col[2][i], font=("Times New Roman",18) )
                    strip[j][i].grid(row=0, column=0, padx=1, pady=1, sticky="news")

                elif( (i==0 or i==10) and (j==0 or j==10) ): #corners

                    bt[j][i]=tk.Button(self.bd, text=[j,i], height="4", width="4", font=("Times New Roman",18) ) #made button
                    bt[j][i].grid(row=j, column=i, padx=1, pady=1, sticky="news") #location of button
                    
        bt[10][10].config(image=self.img[37])    #updating corner buttons with images outside loop cuz of uh difficulties
        bt[10][0].config(image=self.img[38])
        bt[0][0].config(image=self.img[39])
        bt[0][10].config(image=self.img[40])


        self.cp=tk.Label(self.bd, height="475", width="528", image=self.img[45]) #center piece image
        self.cp.place(relx=0.5, rely=0.5, anchor="center")

        self.ch=tk.Button(self.bd, height="200", width="200",bg="#cae8e0", activebackground="#cae8e0", relief="flat",bd=0, image=self.img[46]) #chance button
        self.ch.place(x=397, y=355)
        self.cc=tk.Button(self.bd, height="190", width="200",bg="#cae8e0", activebackground="#cae8e0", relief="flat",bd=0, image=self.img[47]) #community chest button
        self.cc.place(x=100, y=95)


        self.play=tk.Frame(root, bg="black", height="170", width="100", borderwidth="5", highlightbackground="white", highlightthickness=4) #bottom control for the self.player, self.play-frame
        self.play.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0) #this is to position it under the board

        dice_gif=Image.open(PATH + "Images\\image100.gif") #dice gif
        self.diceframes=GUIfxn.loadframes(dice_gif) #to get all the frames of the dice

        self.diceholder=tk.Frame(self.play, height="135", width="255", bg="white") #for white border
        self.diceholder.place(x=615, y=10)

        self.dice1=tk.Label(self.diceholder, height="120", width="120", bg="black") #dice 1 left dice
        self.dice1.place(x=5, y=5)
        self.dice2=tk.Label(self.diceholder, height="120", width="120", bg="black") #dice 2 right dice
        self.dice2.place(x=125, y=5)
        
        self.running=[False] #gif status

        self.diceimg=[0,self.img[48],self.img[49],self.img[50],self.img[51],self.img[52],self.img[53]] #list of dice images

        self.roll=tk.Button(self.play, text="ROLL", bg="white", font=("Times New Roman", 15), command=partial (self.diceroll, [random.randint(1,6),random.randint(1,6),0] )) #Roll Dice
        self.roll.place(x=520, y=50)

        self.plinfo=tk.Label(self.play, text="PLAYER"+str(self.player), height=1, width=12, font=("Times New Roman", 20), fg="white", bg="black", highlightthickness=3, highlightbackground="white")    #self.player tag
        self.plinfo.place(x=270, y=10)

        self.bal=tk.Label(self.play, text="BALANCE: $1500 ", height=2, width=15, font=("Times New Roman", 16), fg="white", bg="black", highlightthickness=3, highlightbackground="white")  #Balance
        self.bal.place(x=30, y=20)

        ow=["ELECTRICAL COMPANY", "BALTIC AVENUE"] #all owned properties which will change the owned screen
        self.own=tk.Button(self.play, text="OWNED", bg="white", font=("Times New Roman", 15), command=partial(GUIfxn.owned, self.player, ow) )  #Owned property
        self.own.place(x=80, y=90)

        self.buy=tk.Button(self.play, text="BUY", height=1, width=7, bg="white", font=("Times New Roman", 15), command=self.playgif )  #Buy Property
        self.buy.place(x=275, y=90)

        self.notbuy=tk.Button(self.play, text="PASS", height=1, width=7,  bg="white", font=("Times New Roman", 15) ,command=self.playgif)  #Pass and not buy
        self.notbuy.place(x=375, y=90)

        self.loc=[[640, 585], [558, 585], [498, 585], [442, 585], [384, 585], [324, 585], [265, 585], [207, 585], [145, 585], [87, 585], [5, 585], 
        [5, 508], [5, 456], [5, 403], [5, 350], [5, 297], [5, 243], [5, 189], [5, 137], [5, 83], [5, 7], [87, 7], [145, 7], [207, 7], [265, 7], 
        [324, 7], [384, 7], [442, 7], [498, 7], [558, 7], [640, 7], [640, 83], [640, 137], [640, 189], [640, 243], [640, 297], [640, 350], 
        [640, 403], [640, 456], [640, 508]]

        self.carl=['' for i in range(0,4)] #initiazlizing pictures of self.player icons
        for i in range(0,len(final)):
            self.carl[i]=tk.Label(self.bd,height="20",width="20", bg=final[i][1], image=self.img[41+i])

        #initializing the starting positons
        start_pos=[[640,585],[665,585],[640,610],[665,610]]
        for i in range(len(final)):
            self.carl[i].place(x=start_pos[i][0], y=start_pos[i][1]) #top left-car, top right-ship, bot left-hat, bot right-dog

        self.cor=[[0,0],[25,0],[0,25],[25,25]] #player image correction
        self.iss=2 #self.iss - i show speed

    def playgif(self): #plays the gif or a dice animation
        
        if(self.running[0]==False): #to prevent multiple animations
            self.running[0]=True

            self.roll.config(state="normal")
            self.buy.config(state="disabled")
            self.notbuy.config(state="disabled")

            GUIfxn.updateframes(self.dice1, self.diceframes, 0, self.running) #updating frames of dice
            GUIfxn.updateframes(self.dice2, self.diceframes, 0, self.running)

    def diceroll_img(self, lbl1, lbl2, rl1, rl2, img): #final two images of dice roll as per ur input, lbl1/2-label of dice, always const., self.img-images of all dices, rl1/2-roll of the dice u want
        self.running[0]=False
        if(rl1 == 0 or rl2==0):
            return
        lbl1.config(image=img[rl1]) #label 1 aka dice 1
        lbl2.config(image=img[rl2]) #label 2 aka dice 2

    def optimus(self, player, spacei, roll): #movement fxn, space i is the initial space
        
        x1=self.loc[(spacei + roll)%40][0] #final destination
        y1=self.loc[(spacei + roll)%40][1]

        def moveth(space, spacex, spacey):
            
            x2=self.loc[(space)%40][0] #position to go to (the coords of the tile after the tile its on)
            y2=self.loc[(space)%40][1]

            if(spacex==x2 and spacey==y2): #if the piece has moved thru a property it will update space or tile id to get the next coords
                space=(space+1)%40 
                x2=self.loc[(space)%40][0]
                y2=self.loc[(space)%40][1]
                
            if(x1==spacex and y1==spacey):
                return

            elif((space>0 and space<=10)): #bot row movement
                self.carl[player].place(x=spacex-1+self.cor[player][0], y=spacey+self.cor[player][1]) #moves the self.player/image by one in the direction
                self.root.after(self.iss, moveth, space, (spacex-1), spacey) #call itself after some time for the animation, it updates the space its on if needed and also changes the x or y coord by 1 every time u call it

            elif((space>20 and space<=30)): #top row movement
                self.carl[player].place(x=spacex+1+self.cor[player][0], y=spacey+self.cor[player][1])
                self.root.after(self.iss, moveth, space, (spacex+1), spacey)

            elif((space>10 and space<=20)): #left column movement
                self.carl[player].place(x=spacex+self.cor[player][0], y=spacey-1+self.cor[player][1])
                self.root.after(self.iss, moveth, space, spacex, (spacey-1))

            elif((space>30 and space<40) or space==0): #right column movement
                self.carl[player].place(x=spacex+self.cor[player][0], y=spacey+1+self.cor[player][1])
                self.root.after(self.iss, moveth, space, spacex, (spacey+1))

        moveth(spacei, self.loc[spacei][0], self.loc[spacei][1])

    def diceroll(self, list): #displays image of dice and then optimus

        self.roll.config(state="disabled")
        space=list[3]
        roll1=list[1]
        roll2=list[2]
        self.diceroll_img(self.dice1, self.dice2, roll1, roll2, self.diceimg)
        
        self.root.after(200, self.optimus(list[0], space, roll1+roll2)) #calls optimus after a delay
        
    def ui_owned(self, player, ow): #ow=["BALTIC AVENUE", "ELECTRICAL COMPANY"] #ow is the list of the properties which u have to give in the fxn along with which self.player

        self.own.config(command=partial(GUIfxn.owned, player, ow))
    
    def ui_bal(self, money): #money in player control ui
        self.bal.config(text="BALANCE: $"+ str(money))

    def ui_plinfo(self, text): #player info changing
        self.plinfo.config(text=text)

    def ui_btn(self, text): #Enter a string to change the text on the buy button
        self.buy.config(text=text)

    def bd_col(self, col): #background colour
            self.play.config(highlightbackground=col)
            self.plinfo.config(highlightbackground=col)
            self.bal.config(highlightbackground=col)
            self.diceholder.config(bg=col)

    def blink(self, col, num, count): #blinking function
        if(count in range(0,num*2+1,2)):
            self.bd_col(col)
            self.plinfo.after(100, self.blink, col, num, count+1)
        elif(count in range(1,num*2,2)):
            self.bd_col("white")
            self.plinfo.after(100, self.blink, col, num, count+1)
        else:
            return

    def moneycountdown(self, m1, m2, count): #moneycountdown animation m1=final, m2=initial
        if(m1==m2):
            return
        if(m2>m1):
            m2-=count
            if(m1>m2):
                m2=m1
        elif(m2<m1):
            m2+=count
            if(m1<m2):
                m2=m1
        count+=10
        self.ui_bal(m2)
        self.plinfo.after(100, self.moneycountdown, m1, m2, count )       

    def chancom(self, img_n): #shows images of chance and community chest, enter image number as parameter
        
        plant=tk.Toplevel()
        plant.title("Card")
        plant.config(bg="black")
        #plant.resizable(False,False)
        c_img=tk.Label(plant, height=181, width=305, bg="black", image=self.img[img_n])
        c_img.pack(padx=10, pady=10)
        
        plant.after(7000, plant.destroy)

    def build(self, prop, tier):
       
        try:
            search=list(properties.loc[prop])
        except:
            return
        
        if(tier==1): #creation of dictionary to store houses
            self.house[prop]=[]

        elif(tier==5): #checks for hotel, deletes all houses and makes a hotel
            for i in self.house[prop]:
                i.destroy()
            hotel=tk.Label(self.bd, bg="black", image=self.img[88]) #creation of hotel label
            hotel.place( x=int(search[9]), y=int(search[10]) )
            return 
        
        hs=tk.Label(self.bd, bg="black", image=self.img[87]) #creation of house label

        if(int(search[9]) in [66,616]): #checks if property is in vertical row
            hs.place( x=int(search[9]), y=int(search[10])+14*(tier-1) )
        else:
            hs.place( x=int(search[9])+14*(tier-1), y=int(search[10]) )
        
        self.house[prop].append(hs)

    
