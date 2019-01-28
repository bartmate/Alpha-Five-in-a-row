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
