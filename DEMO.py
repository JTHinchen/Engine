from random import*

def sideCheck(room,grid): #takes a room (coords) and grid (list of room coords) and returns the rooms adjacent (up down left right) that are turned OFF
    openBorders=[]
    borders=[(room[0]+1,room[1]),(room[0]-1,room[1]),(room[0],room[1]-1),(room[0],room[1]+1)]
    for room in borders:
        if room in grid and grid[room]==0:
            openBorders.append(room)
    return openBorders

class Map:
    def __init__(self):
        XMax=10#Maximum length/height of map
        YMax=10
        chance=12 #base chance (1/chance) that a given room will be generated
        minRooms=15 #minimum number of rooms created
        self.grid={}
        for i in range(XMax): #creates x by y gird of rooms, all turned OFF
            for j in range(YMax):
                self.grid[(i,j)]=0 
        self.start=(int(XMax/2),int(YMax/2)) #room in center is turned ON
        self.grid[self.start]=1
        self.rooms=[self.start]
        self.emprm=[]#ugh theres no good way to pass by value is there
        end=0
        n=0
        while end==0: #repeats until desired number of rooms is reached or surpassed
            for room in self.rooms: #checks all ON rooms
                for empty in sideCheck(room,self.grid): #checks list of OFF rooms bordering current ON
                    #chanceMod=chance/(len(sideCheck(empty,self.grid))+1)           #modifies chance room will be generated, currently gives higher chance torooms bordering more OFFs
                    if len(sideCheck(empty,self.grid))<3:                           #The current mod creates generally non-looping, very branched narrow paths
                           chanceMod=100000
                    else:
                           chanceMod=2
                    if randrange(chanceMod)==0: #turns room ON and adds to list of ONs
                        self.grid[empty]=1
                        self.rooms.append(empty)
                        self.emprm.append(empty)
                        n+=1
            if n>=minRooms:
                end=1
    def display(self,c1=0,c2=0,obj=0): #makes X grid, demonstration only (could do a minimap I guess)
        d={}
        for i in range(10): #i and j are switched from tradtional vector notation. oops.
            d[i]=[]
            for j in range (10):
                if self.grid[(j,i)]==1:
                    d[i].append('|O')
                else:
                    d[i].append('| ')
        if obj !=0:
            for i in obj:
                    d[i[1]][i[0]]=obj[i]
        if c1 !=0:
            d[c1.pos[1]][c1.pos[0]]=c1.sym
        if c2 !=0:
            d[c2.pos[1]][c2.pos[0]]=c2.sym
            if c1.pos==c2.pos:
                d[c2.pos[1]][c2.pos[0]]='|X'
        for i in range(10):
            for j in range(10):
                print (d[i][j],end="")
            print()
            
class Char:
    def __init__(self,Map,name,sym):
        self.pos=Map.start
        self.name=name
        self.sym=sym
        self.inv=[]
    def move(self,Game):
        end=0
        while end==0:
            end=1#
            directions=[(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]-1),(self.pos[0],self.pos[1]+1)]
            print ('\nYou are in a maze.')
            for i in Game.obj:
                if self.pos==i:
                    print ('There is a', Game.terms[Game.obj[i]],'in the room')
            if self.pos==self.otherChar(Game).pos:
                print (self.otherChar(Game).name, 'is in the room') 
            dirc=input(self.name+': What would you like to do?\n')
            if dirc=='pick up' and self.pos in Game.pickup.keys():
                self.inv.append(Game.terms[Game.obj.pop(self.pos)])
                end=0
            elif dirc=='use' and self.pos in Game.fix.keys():
                if Game.terms[Game.fix[self.pos]]=='door':
                    if 'key' in self.inv:
                        print ('You have opened the door')
                        self.inv.remove('key')
                        Game.nextl=1
                    else:
                        print ('The door is locked')
                        end=0
            elif dirc=='stuff':
                if len(self.inv)>0:
                    print ('You have: ', end="")
                    for i in self.inv:
                        print(i,' ',end="")
                    print()
                else:
                    print ('You have nothing')
                end=0
            elif dirc=='up' and directions[2] in Game.world.rooms:
                self.pos=directions[2]
                Game.world.display(Game.c1,Game.c2,Game.obj)
            elif dirc=='down' and directions[3] in Game.world.rooms:
                self.pos=directions[3]
                Game.world.display(Game.c1,Game.c2,Game.obj)
            elif dirc=='left' and directions[1] in Game.world.rooms:
                self.pos=directions[1]
                Game.world.display(Game.c1,Game.c2,Game.obj)
            elif dirc=='right' and directions[0] in Game.world.rooms:
                self.pos=directions[0]
                Game.world.display(Game.c1,Game.c2,Game.obj)
            elif dirc=='wait':
                end=1
            else:
                print("You can't do that!")
                end=0#
    def otherChar(self,Game):
        if self.name==Game.chars[Game.c1]:
            return Game.c2
        elif self.name==Game.chars[Game.c2]:
            return Game.c1
    def reset (self,Game):
        self.pos=Game.world.start

class Game:
    def __init__(self):
        self.world=Map()
        self.c1=Char(self.world,"Char 1",'|/')
        self.c2=Char(self.world,"Char 2",'|\\')
        self.chars={self.c1:self.c1.name,self.c2:self.c2.name}
        self.terms={'|k':'key','|D':'door'}
        self.newLev()
    def newLev (self):
        self.world=Map()       
        self.nextl=0
        self.obj={}
        self.fix={}
        self.pickup={}
        keypos=self.world.emprm[randrange(len(self.world.emprm))]
        self.pickup[keypos]='|k'
        self.world.emprm.remove(keypos)
        doorpos=self.world.emprm[randrange(len(self.world.emprm))]
        self.fix[doorpos]='|D'
        self.world.emprm.remove(doorpos)
        self.obj=self.pickup.copy()
        self.obj.update(self.fix)
        for char in self.chars:
            char.reset(self)
    def run(self):
        self.world.display(self.c1,self.c2,self.obj)
        end=0
        while end!='no':
            for i in self.chars:
                i.move(self)
                if self.nextl==1:
                    if input("Continue?\n")=='no':
                        end='no'
                        break
                    self.newLev()
        print ('Bye!')                 

a=Game()
a.run()
