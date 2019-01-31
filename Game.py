import numpy as np

EMPTY = 0
X = 1
O = 2
DRAW = 3

class Game:
    def __init__(self):
        self.grid   = np.zeros( (15,15), dtype = 'int8') 
        self.moves  = np.zeros( (225,2), dtype = 'int8')
        self.nr     = 0
        self.winner = 0
        self.next   = X
    
    
    def move(self,x,y):
        if self.winner != 0:
            print("ERROR: The game has already ended.")
            return -1
        if self.grid[x,y]!=0:
            print("ERROR: The square is already occupied.")
            return -1
        self.grid[x,y] = self.next
        self.moves[self.nr,0]=x
        self.moves[self.nr,1]=y
        self.nr += 1
        if self.check_win(x,y,self.next):
            self.winner = self.next
        elif self.nr == 225:
            self.winner = DRAW
        self.next = 3-self.next
        return self.winner
        
    def unmove(self):
        self.nr -= 1
        x = self.moves[self.nr,0] #some garbage remains, but it does not count (in theory)
        y = self.moves[self.nr,1]
        self.grid[x,y]=0
        self.winner = 0
        self.next = 3-self.next
        
    def fill_grids_for_nn(self,nn_input): 
        #nn_input: Input for NN, containing one position (shape: (1,15,15,4))
        for x in range(15):
            for y in range(15):
                #grid-x
                nn_input[0,x,y,0] = 0
                if self.grid[x,y]==1:
                    nn_input[0,x,y,0] = 1
                #grid-o
                nn_input[0,x,y,1] = 0
                if self.grid[x,y]==2:
                    nn_input[0,x,y,1] = 1
                #grid-next
                nn_input[0,x,y,2] = self.next-1.0                
                #grid-last
                nn_input[0,x,y,3] = 0
        if self.nr>0:
            nn_input[0,self.moves[self.nr-1,0], self.moves[self.nr-1,1],3] = 1                 
        
    def check_win(self,x,y,curr):
        #horizontal
        l = 1
        xx = x
        yy = y
        while (l<5 and xx+1<15 and self.grid[xx+1,yy]==curr):
            xx += 1
            l += 1
        xx = x
        yy = y
        while (l<5 and xx-1>=0 and self.grid[xx-1,yy]==curr):
            xx -= 1
            l += 1
        if (l>=5):
            return True

        #vertical
        l = 1
        xx = x
        yy = y
        while (l<5 and yy+1<15 and self.grid[xx,yy+1]==curr):
            yy += 1
            l += 1
        xx = x
        yy = y
        while (l<5 and yy-1>=0 and self.grid[xx,yy-1]==curr):
            yy -= 1
            l += 1
        if (l>=5):
            return True
    
        #diag: \
        l = 1
        xx = x
        yy = y
        while (l<5 and xx+1<15 and yy+1<15 and self.grid[xx+1,yy+1]==curr):
            xx += 1
            yy += 1
            l += 1
        xx = x
        yy = y
        while (l<5 and xx-1>=0 and yy-1>=0 and self.grid[xx-1,yy-1]==curr):
            xx -= 1
            yy -= 1
            l += 1
        if (l>=5):
            return True

        #diag: /
        l = 1
        xx = x
        yy = y
        while (l<5 and xx+1<15 and yy-1>=0 and self.grid[xx+1,yy-1]==curr):
            xx += 1
            yy -= 1
            l += 1
        xx = x
        yy = y
        while (l<5 and xx-1>=0 and yy+1<15 and self.grid[xx-1,yy+1]==curr):
            xx -= 1
            yy += 1
            l += 1
        if (l>=5):
            return True
        
        return False
    
    
    def print(self):
        print("-----------------")
        for y in range(15):
            str = '|'
            for x in range(15):
                if self.grid[x,y]==0:
                    str += ' '
                elif self.grid[x,y]==X:
                    str += 'X'
                else:
                    str += 'O'
            str += "|"
            print(str)
        print("-----------------")
