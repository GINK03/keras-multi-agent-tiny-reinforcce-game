from __future__ import print_function
from keras.models import Sequential, load_model, Model
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU, SimpleRNN, Input, RepeatVector
from keras.layers.core import Dropout, Lambda, Flatten, Reshape
from keras.optimizers import RMSprop, Adam, SGD
from keras.utils.data_utils import get_file
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.wrappers import Bidirectional as Bi
from keras.layers.wrappers import TimeDistributed as TD
from keras.engine.topology import Layer
from keras import backend as K
from keras.layers.merge import Concatenate
import numpy as np
import random
import sys
import glob
import pickle
import re

inputs_1_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_1_1 )
x           = Flatten()(x)
x           = Dense(4000, activation='relu')( x )
x           = Dense(16, activation='linear')( x )
x           = Reshape((4,4))(x)
player1     = Model( inputs_1_1, x )
player1.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 

inputs_2_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_2_1 )
x           = Flatten()(x)
x           = Dense(4000, activation='relu')( x )
x           = Dense(16, activation='linear')( x )
x           = Reshape((4,4))(x)
#print(x.shape)
player2     = Model( inputs_2_1, x )
player2.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] )

#optimizers = [SGD(), Adam(), RMSprop()]
