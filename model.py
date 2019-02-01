from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam

import params

FEATNR   = params.MODEL_FEATNR
HIDDENNR = params.MODEL_HIDDENNR
CONVNR   = params.MODEL_CONVNR

class AmoebaZeroModel:
    def __init__(self):  
        self.input = np.zeros((1,15,15,4)) #Input for evaulating one position
        
        # The NN model
        inp = Input((15,15,4))

        #1st conv layer
        x = Conv2D(FEATNR, (3, 3), padding = 'SAME', kernel_regularizer=regularizers.l2(0.01))(inp)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)

        #middle conv layers
        for i in range(CONVNR-2):                
            x = Conv2D(FEATNR, (3, 3), padding = 'SAME', kernel_regularizer=regularizers.l2(0.01))(x)
            x = BatchNormalization()(x)
            x = Activation('relu')(x)

        #last conv layer
        x = Conv2D(FEATNR, (3, 3), padding = 'SAME', kernel_regularizer=regularizers.l2(0.01))(x)
        x = BatchNormalization()(x)
        base = Activation('relu')(x)
        
        x1 = Conv2D(1, (3, 3), padding = 'SAME', kernel_regularizer=regularizers.l2(0.01))(base)
        x1 = BatchNormalization()(x1)
        x1 = Activation('relu')(x1)
        x1 = Flatten()(x1)
        out_p = Dense(225, activation = 'softmax', name = 'out_p', kernel_regularizer=regularizers.l2(0.01))(x1)
        
        x2 = Conv2D(1, (3, 3), padding = 'SAME', kernel_regularizer=regularizers.l2(0.01))(base)
        x2 = BatchNormalization()(x2)
        x2 = Activation('relu')(x2)
        x2 = Flatten()(x2)
        x2 = Dense(HIDDENNR, activation = 'relu', kernel_regularizer=regularizers.l2(0.01))(x2)
        out_v = Dense(1, activation = 'sigmoid', name = 'out_v', kernel_regularizer=regularizers.l2(0.01))(x2)
        
        self.model = Model(inputs = inp, outputs = [out_p,out_v])
        
        losses = { "out_p": "categorical_crossentropy", "out_v": "mse"}
        lossWeights = {"out_p": 1.0, "out_v": 1.0}
        
        opt = Adam()
        
        self.model.compile(optimizer=opt, loss=losses, loss_weights=lossWeights,
                          metrics={"out_p": "categorical_crossentropy", "out_v": "mse"})
    
    def evaluate(self, game, verbose = 0):
        game.fill_grids_for_nn(self.input)
        pred = self.model.predict(self.input, verbose = verbose)
        return pred[0][0].reshape((15,15)), pred[1][0][0]
    
    
    def train(self,X,Y,batch_size = 64, epoch_nr = 1):
        self.model.fit(x=X, y=Y, batch_size=batch_size, epochs=epoch_nr)
    
