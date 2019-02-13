import numpy as np

# Width/height of the grid
N = 7

# Grid-width square
NN = N*N

# Number of X-s (or O-s) to win
WN = 4

EMPTY = 0
X = 1
O = 2
DRAW = 3

class Game:
    def __init__(self):
        self.grid   = np.zeros( (N,N), dtype = 'int8') 
        self.moves  = np.zeros( (NN,2), dtype = 'int8')
        self.nr     = 0
        self.winner = 0
        self.next   = X
    
    
    def move(self,x,y):
        assert (self.winner == 0), "ERROR: The game has already ended."        
        assert (self.grid[x,y]==0), "ERROR: The square is already occupied."        
        self.grid[x,y] = self.next
        self.moves[self.nr,0]=x
        self.moves[self.nr,1]=y
        self.nr += 1
        if self.check_win(x,y,self.next):
            self.winner = self.next
        elif self.nr == NN:
            self.winner = DRAW
        self.next = 3-self.next
        return self.winner
        
    def unmove(self):
        assert (self.nr > 0), "ERROR: Game not started, no move to undo."        
        self.nr -= 1
        x = self.moves[self.nr,0] #some garbage remains, but it does not count (in theory)
        y = self.moves[self.nr,1]
        self.grid[x,y]=0
        self.winner = 0
        self.next = 3-self.next
        
    def fill_grids_for_nn(self,nn_input,ind=0): 
        #nn_input: Input for NN, containing one position (shape: (?,N,N,4))
        for x in range(N):
            for y in range(N):
                #grid-x
                nn_input[ind,x,y,0] = 0
                if self.grid[x,y]==1:
                    nn_input[ind,x,y,0] = 1
                #grid-o
                nn_input[ind,x,y,1] = 0
                if self.grid[x,y]==2:
                    nn_input[ind,x,y,1] = 1
                #grid-next
                nn_input[ind,x,y,2] = self.next-1.0                
                #grid-last
                nn_input[ind,x,y,3] = 0
        if self.nr>0:
            nn_input[ind,self.moves[self.nr-1,0], self.moves[self.nr-1,1],3] = 1                 
            
    def get_final_value(self):
        assert (self.winner != 0), "ERROR: Game has not been ended, no final value yet."
            
        if self.winner == X:
            return 0.0
        elif self.winner == O:
            return 1.0
        else:
            return 0.5
        
    def check_win(self,x,y,curr):
        #horizontal
        l = 1
        xx = x
        yy = y
        while (l<WN and xx+1<N and self.grid[xx+1,yy]==curr):
            xx += 1
            l += 1
        xx = x
        yy = y
        while (l<WN and xx-1>=0 and self.grid[xx-1,yy]==curr):
            xx -= 1
            l += 1
        if (l>=WN):
            return True

        #vertical
        l = 1
        xx = x
        yy = y
        while (l<WN and yy+1<N and self.grid[xx,yy+1]==curr):
            yy += 1
            l += 1
        xx = x
        yy = y
        while (l<WN and yy-1>=0 and self.grid[xx,yy-1]==curr):
            yy -= 1
            l += 1
        if (l>=WN):
            return True
    
        #diag: \
        l = 1
        xx = x
        yy = y
        while (l<WN and xx+1<N and yy+1<N and self.grid[xx+1,yy+1]==curr):
            xx += 1
            yy += 1
            l += 1
        xx = x
        yy = y
        while (l<WN and xx-1>=0 and yy-1>=0 and self.grid[xx-1,yy-1]==curr):
            xx -= 1
            yy -= 1
            l += 1
        if (l>=WN):
            return True

        #diag: /
        l = 1
        xx = x
        yy = y
        while (l<WN and xx+1<N and yy-1>=0 and self.grid[xx+1,yy-1]==curr):
            xx += 1
            yy -= 1
            l += 1
        xx = x
        yy = y
        while (l<WN and xx-1>=0 and yy+1<N and self.grid[xx-1,yy+1]==curr):
            xx -= 1
            yy += 1
            l += 1
        if (l>=WN):
            return True
        
        return False
    
    
    def print(self):
        s = ' '
        for i in range(N):
            s += chr(65+i)
        print(s)
                
        
        print("-----------------")
        for y in range(N):
            s = '|'
            for x in range(N):
                if self.grid[x,y]==0:
                    s += ' '
                elif self.grid[x,y]==X:
                    s += 'X'
                else:
                    s += 'O'
            s += "|" + str(y+1)            
            print(s)
        print("-----------------")

        