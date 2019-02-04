import numpy as np
import copy

from Game import * 
import params

class Node:
    def __init__(self):
        self.edges = []
        
class Edge:
    def __init__(self, x, y, node = None, p = 0.0):
        self.N = 0
        self.W = 0.0
        self.Q = 0.0
        self.P = p
        self.act_x = x
        self.act_y = y
        self.result_node = node       
        
class MCTS:
    def __init__(self, game, evaluator, root_node = None):
        self.root_node = root_node
        if self.root_node is None:
            self.root_node = Node()
        self.game = copy.deepcopy(game)
        self.evaluator = evaluator   
    
    def reinit(self, game, node):
        self.root_node = node
        self.game = copy.deepcopy(game)
            
    def select_move(self, competitive = False):
        for i in range(params.MCTS_NR):
            self.reach_leaf_node_and_update_edges_and_extend()
        if competitive:
            maxN = -1
            arr = []
            for edge in self.root_node.edges:
                if edge.N > maxN:
                    maxN = edge.N
                    arr=[]
                    arr.append(edge)
                elif edge.N == maxN:
                    arr.append(edge)                    
            edge = np.random.choice(arr)            
        else:
            prob=np.zeros( (len(self.root_node.edges)) )
            for i in range(len(self.root_node.edges)):
                prob[i] = float(self.root_node.edges[i].N)**(1.0/params.MCTS_TAU)
            prob /= sum(prob)
            index = np.random.choice( len(self.root_node.edges), p=prob)
            edge = self.root_node.edges[index]

        return edge.act_x, edge.act_y, edge.result_node

    def reach_leaf_node_and_update_edges_and_extend(self):
        curr = self.root_node
        route = []
        while len(curr.edges) != 0:
            prob=np.zeros( (len(curr.edges)) )
            for i in range(len(curr.edges)):
                Q = curr.edges[i].Q
                U = params.MCTS_U_COEFF * curr.edges[i].P / (1.0 + curr.edges[i].N)
                prob[i] = Q + U
            prob /= sum(prob)
            index = np.random.choice( len(curr.edges), p=prob)
            edge = curr.edges[index]
            route.append(edge)
            curr = edge.result_node
            self.game.move(edge.act_x, edge.act_y)
        
        #In MTCS we use value 1.0 if the next player will win in 100%
        #and 0.0 if the next player will win in 0% (i.e. they [he or she] will lose)
        #
        #So the value depend on the fact who is the next player
        #However the NN gives an absolute value independently on the next player:
        #0.0 - X will win; 1.0 - O will win.
        
        p = None
        if self.game.winner == 1 or self.game.winner == 2:   # X or O
            v = 1.0 #From the perspective of the player who has just played
        elif self.game.winner == 3: # Draw
            v = 0.5 #From the perspective of the player who has just played
        else: # Not terminating state
            p,v = self.evaluator(self.game)
            if self.game.next == 2: #O -> The player who has just played was X
                v = 1.0 - v
            
        # Extending the current node
        if p is not None:
            s = 0.0
            for x in range(15):
                for y in  range(15):
                    if self.game.grid[x,y] == 0:
                        n = Node()
                        e = Edge(x,y,n,p[x,y])
                        curr.edges.append(e)
                        s += p[x,y]
            if s!=0:
                for e in curr.edges:
                    e.P /= s
        
        # Update edges on the route
        for i in range( len(route)-1, -1, -1):
            route[i].N += 1
            route[i].W += v
            route[i].Q = route[i].W / route[i].N
            v = 1.0 - v 
            self.game.unmove()
            
    def fill_p(self, p, ind = 0):
        for x in range(15):
            for y in  range(15):
                if self.game.grid[x,y] == 0:
                    p[ind,x*15+y] = 1.0
                else:
                    p[ind,x*15+y] = 0.0
        for i in range(len(self.root_node.edges)):
            x = self.root_node.edges[i].act_x
            y = self.root_node.edges[i].act_y                
            p[ind,x*15+y] *= float(self.root_node.edges[i].N)**(1.0/params.MCTS_TAU)
        s = np.sum(p[ind,:])
        if s>0:
            p[ind,:] /= s


            