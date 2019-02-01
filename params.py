#Nr. of Simulation in MTCS
MCTS_NR   = 256    

#Temperature for controlling exploration
MCTS_TAU  = 0.5

#Competitieve play: Chosing the node with maximal N (equivalent to TAU = infinitesimally small)
MCTS_COMP = True   

#Coefficient for U in Q+U
MCTS_U_COEFF = 2.0

####################################

# Number of features in each conv layer
MODEL_FEATNR = 16

# Number of hidden units in value head
MODEL_HIDDENNR = 64

# Number of conv layers
MODEL_CONVNR = 5
