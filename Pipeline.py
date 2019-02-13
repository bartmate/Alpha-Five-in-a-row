import numpy as np
import copy
import keras.models

from MCTS import MCTS
from Game import * 
from model import AmoebaZeroModel
import params

HISTORY_SIZE     = params.PIPELINE_HISTORY_SIZE
BATCH_SIZE       = params.PIPELINE_BATCH_SIZE
TRAINING_LOOP_NR = params.PIPELINE_TRAINING_LOOP_NR
SELFPLAY_NR      = params.PIPELINE_SELFPLAY_NR
EVAL_NR          = params.PIPELINE_EVAL_NR
THRESHOLD        = params.PIPELINE_THRESHOLD

class Pipeline:
    def __init__(self, verbose = 0):
        self.verbose = verbose
        
        self.history_input = np.zeros( (HISTORY_SIZE,N,N,4))
        self.history_p     = np.zeros( (HISTORY_SIZE,NN))
        self.history_v     = np.zeros( (HISTORY_SIZE))
        self.batch_input   = np.zeros( (BATCH_SIZE,N,N,4))
        self.batch_p       = np.zeros( (BATCH_SIZE,NN))
        self.batch_v       = np.zeros( (BATCH_SIZE))
        self.next_index    = 0
        self.history_nr    = 0
        self.version       = 0
        
        self.model_trained = AmoebaZeroModel()
        self.model_trained.model.save("./models/saved_model_0.h5")
        
        self.model_best       = AmoebaZeroModel()
        self.model_best.model = keras.models.load_model("./models/saved_model_0.h5")
    
    def main_loop(self):
        nr = 0
        while True:
            print("Loop - ", nr)
            self.self_play()
            self.train()
            if self.evaluate_trained():
                self.version += 1
                self.model_trained.model.save("./models/saved_model_"+str(self.version)+".h5")
                self.model_best.model = keras.models.load_model("./models/saved_model_"+str(self.version)+".h5")
                print("New model saved. Version: ", self.version)
    
    def self_play(self):
        if self.verbose >= 1:
            print("Self play")
        for i in range(SELFPLAY_NR):
            if self.verbose >=2:
                print(i, "start_index = ", self.next_index)
            start_index = self.next_index
            g = Game()
            mcts = MCTS(g, self.model_best.evaluate)
            nr = 0
            while (g.winner==0):
                nr += 1
                x,y,n = mcts.select_move()                
                g.fill_grids_for_nn(self.history_input,self.next_index)
                mcts.fill_p(self.history_p,self.next_index)
                self.next_index = (self.next_index + 1) % HISTORY_SIZE
                if self.history_nr<HISTORY_SIZE:
                    self.history_nr += 1
                g.move(x,y)
                mcts.reinit(g,n)
                if self.verbose>=3:
                    print(nr, "- move: ", x, y, "; next_index: ", self.next_index)
                if i==0 and self.verbose>=4:
                    g.print()
            v = g.get_final_value()

            if self.verbose >= 2:
                print("Result:", g.winner)
            
            i = start_index
            while i != self.next_index:
                self.history_v[i] = v
                i = (i+1)%HISTORY_SIZE
    
    def train(self):
        if self.verbose >= 1:
            print("Train")
        for i in range(TRAINING_LOOP_NR):
            if self.verbose >= 2:
                print("i: " + str(i))
            
            for j in range(BATCH_SIZE):
                ind = np.random.randint(0,self.history_nr)
                self.batch_input[j] = self.history_input[ind]
                self.batch_p[j]     = self.history_p[ind]
                self.batch_v[j]     = self.history_v[ind]
            self.model_trained.train(self.batch_input,[self.batch_p,self.batch_v],BATCH_SIZE)           
            
    def evaluate_trained(self):
        if self.verbose >= 1:
            print("Evaluate")

        balance = 0 #+ if trained, - if best won more
        
        #best begins
        for i in range(EVAL_NR//2):
            if self.verbose >= 2:
                print("i: ",i)
            g  = Game()
            nr = 0
            while (g.winner==0):
                if nr%2==0:
                    mcts = MCTS(g, self.model_best.evaluate)
                    x,y,_ = mcts.select_move()
                    g.move(x,y)
                else:
                    mcts = MCTS(g, self.model_trained.evaluate)
                    x,y,_ = mcts.select_move()
                    g.move(x,y)
                nr+=1
                if i==0 and self.verbose>=4:
                    g.print()
                
            if g.winner == 1:
                balance -= 1
            elif g.winner == 2:
                balance += 1

            if self.verbose >= 2:
                print("Result:", g.winner)

        #trained begins
        for i in range(EVAL_NR//2):
            if self.verbose >= 2:
                print("i: ",i)
            g  = Game()
            nr = 0
            while (g.winner==0):
                if nr%2==0:
                    mcts = MCTS(g, self.model_trained.evaluate)
                    x,y,_ = mcts.select_move()
                    g.move(x,y)
                else:
                    mcts = MCTS(g, self.model_best.evaluate)
                    x,y,_ = mcts.select_move()
                    g.move(x,y)
                nr+=1
                if i==0 and self.verbose>=4:
                    g.print()
            if g.winner == 1:
                balance += 1
            elif g.winner == 2:
                balance -= 1

            if self.verbose >= 2:
                print("Result:", g.winner)

                
        if self.verbose >= 1:
            print("Total result: ",balance," Thr.: ",THRESHOLD)
                
        #return balance >= THRESHOLD
        return balance >= THRESHOLD
           
        
        