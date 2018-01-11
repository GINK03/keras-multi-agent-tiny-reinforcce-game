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
from pprint import pprint
import numpy as np
import random
import sys
import glob
import pickle
import re
import json
import ocero_detection

# white, 1
inputs_1_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_1_1 )
x           = Flatten()(x)
x           = Dense(4000, activation='relu')( x )
x           = Dense(16, activation='linear')( x )
x           = Reshape((4,4))(x)
player1     = Model( inputs_1_1, x )
player1.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 

# black, -1
inputs_2_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_2_1 )
x           = Flatten()(x)
x           = Dense(4000, activation='relu')( x )
x           = Dense(16, activation='linear')( x )
x           = Reshape((4,4))(x)
player2     = Model( inputs_2_1, x )
player2.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] )

#optimizers = [SGD(), Adam(), RMSprop()]
X = [
  [0, 0, 0, 0],
  [0, 1, -1, 0],
  [0, -1, 1, 0],
  [0, 0, 0, 0],
]
y = player1.predict( np.array([X]) )
pprint( y.tolist()[0] )
Xstatus = {index:x for index, x in enumerate(sum(X, []))}
point =  list(filter(lambda x: Xstatus.get(x[0]) == 0, [(index,prob) for index, prob in sorted(enumerate(sum(y.tolist()[0], [])), key=lambda x:x[1]*-1)] ) )[0]
p, _ = point
y = p//4
x = p%4 
X[y][x] = 1
# eval and update playter2
X = ocero_detection.update(X, y, x, type=1)
[print(x) for x in X]
print('-'*10)
# この時の、1, -1の数
size_1_1 = len(list(filter(lambda x:x==1, sum(X, []))))
size_1_2 = len(list(filter(lambda x:x==-1, sum(X, []))))

y = player2.predict( np.array([X]) )
Xstatus = {index:x for index, x in enumerate(sum(X, []))}
point =  list(filter(lambda x: Xstatus.get(x[0]) == 0, [(index,prob) for index, prob in sorted(enumerate(sum(y.tolist()[0], [])), key=lambda x:x[1]*-1)] ) )[0]
p, _ = point
y = p//4
x = p%4 
X[y][x] = -1
# eval and update player1
X = ocero_detection.update(X, y, x, type=-1)
[print(x) for x in X]
print('-'*10)

size_2_1 = len(list(filter(lambda x:x==1, sum(X, []))))
size_2_2 = len(list(filter(lambda x:x==-1, sum(X, []))))
