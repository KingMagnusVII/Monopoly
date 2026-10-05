import tkinter as tk
from functools import partial       #to preload a function without calling it
import functions as fx
import pandas as pd
from PIL import Image, ImageTk
import os
import PATH

PATH= PATH.path #path file addition
os.chdir(PATH + "saves")

properties = pd.read_csv(PATH + "Data-Files\\properties.csv", index_col = 0)

def msg(players, name, color): #pop up function #takes in the player.no and the name and color of the property, need to change the player no a lil bit in the future
    
    if(name==""):
        return
    
    elif(name in ["READING RAILROAD", "PENNSYLVANIA RAILROAD", "B. & O. RAILROAD", "SHORT LINE RAILROAD", "ELECTRIC COMPANY", "WATER WORKS"]):

        stomata=tk.Toplevel()
        stomata.title(name)
        stomata.geometry("320x400")
        stomata.config(bg="black")
        exceptions_={"READING RAILROAD":54, "PENNYSLVANIA RAILROAD":55, "B. & O. RAILROAD":56, "SHORT LINE RAILROAD":57, "ELECTRIC COMPANY":59, "WATER WORKS":58}
        img=Image.open( PATH+f"Images\\image{exceptions_[name]}.png" )
        img=img.resize((260,360), Image.Resampling.LANCZOS)
        exceptions_[name]=ImageTk.PhotoImage(img)
        lb=tk.Label(stomata, height="360", width="260", borderwidth="2", relief="solid", image=exceptions_[name]) # light grey outer card frame - fr, 2 section: top colured part(td), and information part(info)
        lb.pack(padx=20, pady=20)   #placing it with padding
        stomata.mainloop()


    else:
        stem=tk.Tk()
        stem.title(name)
        stem.geometry("320x400") #window creation
        stem.config(bg="black")

                #information display, rent values acc needed
        inf = [
        "Rent: " + str(properties.at[name, 'rent']),
        "With 1 House: " + str(properties.at[name, 'house1']),
        "With 2 Houses: " + str(properties.at[name, 'house2']),
        "With 3 Houses: " + str(properties.at[name, 'house3']),
        "With 4 Houses: " + str(properties.at[name, 'house4']),
        "With Hotel: " + str(properties.at[name, 'hotel']),
        "Mortgage Value: " + str(properties.at[name, 'price'] // 2),
        "House Cost: " + str(properties.at[name, 'housecost']),
        "Hotel Cost: " + str(properties.at[name, 'hotelcost']),
        "If a player owns all sites of any colour group, rent is doubled."
        ]
        
        infor=['' for i in range(0,10)]

        fr=tk.Frame(stem, height="400", width="250", bg="lightgrey", borderwidth="2", relief="solid") # light grey outer card frame - fr, 2 section: top colured part(td), and information part(info)
        fr.pack(padx=20, pady=20)   #placing it with padding
        fr.rowconfigure(0, weight=1)    #initialising 2 rows
        fr.rowconfigure(1, weight=1)

        td=tk.Frame(fr, height="100", width="250", bg=color, borderwidth="2", relief="solid") #top coloured part frame - td (title deed)
        td.grid(row =0, column=0, padx=5, pady=5, sticky="news")    #location of td in master frame fr

        td.columnconfigure(0,weight=1)  #initialising 1 column and 3 rows
        for i in range(0,3):
            td.rowconfigure(i, weight=1)

        td1=tk.Label(td, text="TITLE DEED", bg=color, font=("Times new Roman", 8))   #title deed
        td1.grid(row=0, column=0, sticky="news", padx=1, pady=1)

        td2=tk.Label(td, text=name, bg=color, font=("Times new Roman", 12))     #property name
        td2.grid(row=1, column=0, sticky="news", padx=1, pady=1)

        t=fx.owner(players, name)
        
        if(t!=None):
            t=t.name
            
        else:
            t=""
        td3=tk.Label(td, text="Owned by: "+t, bg=color, font=("Times new Roman", 9))  #owned by
        td3.grid(row=2, column=0, sticky="news", padx=1, pady=1)



        info=tk.Frame(fr, height="300", width="250", bg="white", borderwidth="2", relief="solid")   #information part frame - info
        info.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        info.columnconfigure(0, weight=1) #initialising 1 column and 10 rows
        for i in range(0,10):
            info.rowconfigure(i, weight=1)

        infor[0]=tk.Label(info, text=inf[0], bg="white", font=("Times new Roman", 10))  #Rent: out of loop for different font size
        infor[0].grid(row=0, column=0, sticky="news", padx=1, pady=1)

        for i in range(1,9):      #all rows and information stored in list is displayed using loop
            infor[i]=tk.Label(info, text=inf[i], bg="white", font=("Times new Roman", 8)) 
            infor[i].grid(row=i, column=0, sticky="news", padx=1, pady=1)    #location of row

        infor[9]=tk.Label(info, text=inf[9], bg="white", font=("Times new Roman", 6))   #if all players own... out of loop for different font size
        infor[9].grid(row=9, column=0, sticky="news", padx=1, pady=1)

        stem.mainloop()

def loadframes (gif): #to load all frames of a gif
    from PIL import Image, ImageTk
    frames=[] #list for all frames
    try:
        while True:
            frame=gif.copy() #gets the current frame
            frame=frame.resize((120,120),Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame)) #appends the frame
            gif.seek(len(frames)) #moves onto the next frame since the length of the list is 1 more than the no. of elements
    except EOFError: #error when it has gone through all frames
        return frames 

def updateframes(label, frames, i, running): 
    if(running[0]==True): #to stop if its running
        label.config(image=frames[i]) #changing frame by frame
        i+=1 #need to move next frame
        if(i==len(frames)): #resetting i if it exceeds the number of frames
            i=0
        label.after(100, updateframes, label, frames, i, running) #calling it again to change frame
    
def owned(player, own): #pop up for all properties he owns

    leaf=tk.Tk() #new screen
    leaf.geometry("900x500") 
    leaf.resizable(False, False)
    leaf.config(bg="black")
    leaf.title("OWNED PROPERTIES")
    layt=tk.Frame(leaf, height="500", width="500", bg="black")
    layt.pack(pady=50, padx=5)

    #all properties
    prop=[["BALTIC AVENUE","MEDITERRANEAN AVENUE"],["CONNECTICUT AVENUE","VERMONT AVENUE","ORIENTAL AVENUE"],["VIRGINIA AVENUE","STATES AVENUE","ST. CHARLES PLACE"],
        ["NEW YORK AVENUE","TENNESSEE AVENUE","ST. JAMES PLACE"],["KENTUCKY AVENUE","INDIANA AVENUE","ILLINOIS AVENUE"],["ATLANTIC AVENUE","VENTNOR AVENUE","MARVIN GARDENS"],
        ["PACIFIC AVENUE","NORTH CAROLINA AVENUE","PENNSYLVANIA AVENUE"],["PARK PLACE","BOARDWALK"],["READING RAILROAD","PENNSYLVANIA RAILROAD","B. & O. RAILROAD","SHORT LINE RAILROAD"],["ELECTRICAL COMPANY", "WATER WORKS"]]

    for i in range (0,5): #row and coumn creation
        layt.columnconfigure(i, weight=1)
    for i in range (0,11):
        layt.rowconfigure(i, weight=1)

    bt=[['' for i in range (0,11)] for i in range(0,5) ] #button creation

    col=["brown","lightblue","pink", "orange", "red", "yellow", "green", "blue", "white", "white"] #all colours for header of the rows and columns

    for i in range(0,5): #upper coloured labels

        bt[i][0]=tk.Label(layt, width="50", bg = col[i] ) #upper row
        bt[i][0].grid(row=0, column=i, padx=1, pady=3, rowspan=1, columnspan=1)

        bt[i][6]=tk.Label(layt, width="50", bg = col[i+5] ) #bottom row
        bt[i][6].grid(row=6, column=i, padx=1, pady=3, rowspan=1, columnspan=1)

        simply=tk.Label(layt, bg="black") #label to create gap bw top and bottom row
        simply.grid(row=5, column=2, columnspan=5)

    for i in range(0,5): #buttons 
        p=prop[i]
        for j in range(0,len(p)): #upper row

            bt[i][j+1]=tk.Button(layt, width="50", font=("Times New Roman", 10))
            bt[i][j+1].grid(row=j+1, column=i, padx=3, pady=5, rowspan=1, columnspan=1)
            if(p[j] in own): #if he owns the property then it shows it, else it will be blank
                bt[i][j+1].config(text=p[j], command=partial(msg, player, p[j], col[i])  ) #the function is for when the user clicks the property he owns, it will show a pop up
            else:
                bt[i][j+1].config(state="disabled")

        p=prop[i+5]
        for j in range(0,len(p)): #bottom row

            bt[i][j+7]=tk.Button(layt, width="50", font=("Times New Roman", 10))
            bt[i][j+7].grid(row=j+7, column=i, padx=3, pady=5, rowspan=1, columnspan=1)
            if(p[j] in own): 
                bt[i][j+7].config(text=p[j], command=partial(msg, player, p[j], col[i+5])  )
            else:
                bt[i][j+7].config(state="disabled")
               

    leaf.mainloop()

class Menu:

    def __init__(self, root):
        self.pl_count=2 #default
        self.name=[] #customised names
        self.color=["white","white","white","white"] #def color is white
        self.final=[] #final array to be passed which contains the name and the color

        self.root=root
        self.root.geometry("500x500")
        self.root.config(bg="black")
        self.root.resizable(False, False)
        self.root.title("MONOPOLY MENU")

        self.fr=tk.Frame(self.root, bg="black", highlightcolor="white", highlightthickness=5) #main frame
        self.fr.pack(fill="both", expand=True, padx=10, pady=10)

        intro=tk.Label(self.fr, height=2, width=10, text="MONOPOLY", font=("Times New Roman", 30), bg="black", fg="white") #MONOPOLY
        intro.place(anchor="center", x=240, y=50)

        self.pl_fr=tk.Frame(self.fr, bg="black", height=200, width=300) #player pop up for name and color
        self.pl_fr.place(x=100, y=180)

        self.p=[] #names array
        self.col_bt=[] #all color buttons array
        self.col=["red","orange","yellow","lightgreen","green","blue","lightblue","purple","violet","pink","white","black"] #color pallette

        
        pl_count=tk.Label(self.fr, text="PLAYERS", font=("Times New Roman", 20), bg="black", fg="white") #PLAYER 
        pl_count.place(x=90, y=120)
        pl_bt=['','','','']
        for i in range(3):
            pl_bt[i]=tk.Button(self.fr, height=2, width=4, text=str(i+2), font=("Times New Roman", 10), bg="black", fg="white", command=partial(self.plrow, i+2)) #buttons for 2,3,4 players
            pl_bt[i].place(x=230 + (50*i), y=120)
        pl_bt[3]=tk.Button(self.fr, height=2, width=4, text="S", font=("Times New Roman", 10), bg="black", fg="white", command=self.load) #S button
        pl_bt[3].place(x=380, y=120)

        #FINAL STEP, after continue is pressed, it will get all the values
        conti=tk.Button(self.fr, height=2, width=10, text="CONTINUE", font=("TIMES NEW ROMAN", 10), bg="black", fg="white", relief='raised', command=self.get_input)
        conti.place(x=200, y=400)

    def plrow(self, n): #player rows, player inputs dropdown

            self.pl_count=n
            self.pl_fr.destroy() #to destroy the previous dropdown if the player switches
            self.pl_fr=tk.Frame(self.fr, bg="black", height=200, width=300)
            self.pl_fr.place(x=100, y=180)

            for i in range(n+1):
                self.pl_fr.rowconfigure(i, weight=1)

            self.p=[['','']] #1st row for the PLAYER NAME and COLOUR
            self.p.extend(['' for i in range(n)]) #for initialisation, contains all empty boxes

            self.p[0][0]=tk.Label(self.pl_fr, text="PLAYER NAME", font=("Times New Roman", 15), bg="black", fg="white")
            self.p[0][0].grid(row=0, column=0, padx=5, pady=5)
            self.p[0][1]=tk.Label(self.pl_fr, text="PLAYER COLOUR", font=("Times New Roman", 15), bg="black", fg="white")
            self.p[0][1].grid(row=0, column=1, pady=5)

            col_fr=['' for i in range(n)] #colour frames to hold the colour buttons
            self.col_bt=[['' for i in range (len(self.col))] for i in range(n)] #colour buttons

            for i in range(1,n+1):
                self.p[i]=tk.Entry(self.pl_fr, width=11, font=("Times New Roman", 18), bg="black", fg="white", insertbackground="white") #input box
                self.p[i].grid(row=i, column=0, pady=5) 
                col_fr[i-1]=tk.Frame(self.pl_fr, bg="black") #modding frames
                col_fr[i-1].grid(row=i, column=1)
                for j in range(len(self.col)): #creation of the colour pallette to hold the colour buttons
                    self.col_bt[i-1][j]=tk.Button(col_fr[i-1], bg=self.col[j]) #colour button modding
                    self.col_bt[i-1][j].config(command=partial(self.col_input, i-1, j)) #to load itself with the colour prematurely
                    self.col_bt[i-1][j].grid(row=i, column=j, padx=1)

    def get_input(self): #gets all the names entered 
        for i in range(1,self.pl_count+1):
            self.name.append(self.p[i].get())
        for i in range(len(self.name)):
            self.final.append([self.name[i], self.color[i]])
        self.root.destroy() #after getting the input it deletes the menu
        
    def col_input(self, i,j): #gets all the colurs entered and set all the btn states to normal and disable the button pressed
        self.color[i]=self.col[j]
        for k in range(12):
            self.col_bt[i][k].config(state="normal")
        self.col_bt[i][j].config(state="disabled")

    def load(self): #menu of lists of saves

        root=tk.Toplevel()
        root.title("Loads")
        root.resizable(False,False)
        root.config(bg="black")
        root.geometry("450x500")

        f1=tk.Frame(root, bg="black")
        f1.pack(fill="both", expand=True)

        cn=tk.Canvas(f1, bg="black", highlightcolor="white", highlightthickness=3)
        cn.pack(side="left",expand=True, fill="both", padx=(10,5), pady=10, ipadx=10, ipady=10)

        sc=tk.Scrollbar(f1, orient="vertical", command=cn.yview, width=20)
        sc.pack(fill="y", side="right", padx=(1,10), pady=10)
        cn.configure(yscrollcommand=sc.set)

        f2=tk.Frame(cn, bg="black")
        window_id = cn.create_window((0,0),window=f2, anchor="nw")

        nfs=os.listdir()

        def loadbtn(filename): #loadbtn functions
            self.final=["S",filename]
            self.root.destroy()

        def delbtn(filename): #delete button function
            os.remove(filename)
            root.destroy()
            self.load()

        cf=[] #all content frames
         
         #all frames creates made into a function to dynamically update after deletion
        for i in range(len(nfs)):
            cf.append("")
            cf[i]=tk.Frame(f2,highlightthickness=3, highlightcolor="white", bg="black")
            cf[i].pack(fill="x", padx=5, pady=5)
            lb=tk.Label(cf[i], text=nfs[i], font=("Times New Roman", 18), bg="black", fg="white")
            lb.pack(fill="x", anchor="center", pady=(10,0))
            bt1=tk.Button(cf[i], text="Load", font=("Times New Roman",15), width=8, bg="black", fg="white", command=partial(loadbtn, nfs[i])) #load btn
            bt1.pack(side="left", pady=10, padx=(65,5))
            bt2=tk.Button(cf[i], text="Delete", font=("Times New Roman",15), width=8, bg="black", fg="white", command=partial(delbtn, nfs[i])) #delete btn
            bt2.pack(side="right", pady=10, padx=(5,65))

        def update_scrollregion(event):
            cn.configure(scrollregion=cn.bbox("all")) #adjust scroll
            cn.itemconfig(window_id, width=cn.winfo_width()) #adjust the f2 width

        f2.bind("<Configure>", update_scrollregion)
        cn.bind("<Configure>", update_scrollregion)  
        cn.bind_all("<MouseWheel>", lambda e: cn.yview_scroll(-1*(e.delta//120), "units"))

        root.mainloop()

def runmenu():
    root=tk.Tk()
    menu=Menu(root)
    root.mainloop()
    return menu.final



