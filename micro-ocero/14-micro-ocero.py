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
import copy

# white, 1
inputs_1_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_1_1 )
x           = Dropout(0.3)(x)
x           = Dense(4000, activation='relu')( x )
x           = Flatten()(x)
x           = Dense(16, activation='linear')( x )
x           = Reshape((4,4))(x)
player1     = Model( inputs_1_1, x )
player1.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 

# black, -1
inputs_2_1  = Input( shape=(4,4) ) 
x           = Dense(4000, activation='relu')( inputs_2_1 )
x           = Dropout(0.3)(x)
x           = Dense(4000, activation='relu')( x )
x           = Flatten()(x)
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
size_1_1, size_1_2, size_2_1, size_2_2 = 2, 2, 2, 2 

for k in range(1000000):
  if all([ x!=0 for x in sum(X, [])] ): 
    [print(x) for x in X]
    size_1 = len(list(filter(lambda x:x==1, sum(X, []))))
    size_2 = len(list(filter(lambda x:x==-1, sum(X, []))))
    # y1を強化する
    if size_1 > size_2:
      y, x = y1p
      y1[0][y][x] = y1[0][y][x]*5.0
      player1.fit( np.array([y1X]), y1 )
    else:    
      y, x = y1p
      y1[0][y][x] = y1[0][y][x]*0.1
      player1.fit( np.array([y1X]), y1 )
    X = [
      [0, 0, 0, 0],
      [0, 1, -1, 0],
      [0, -1, 1, 0],
      [0, 0, 0, 0],
    ]
    size_1_1, size_1_2, size_2_1, size_2_2 = 2, 2, 2, 2 
    
  y1 = player1.predict( np.array([X]) )
  #pprint( y1.tolist()[0] )
  Xstatus = {index:x for index, x in enumerate(sum(X, []))}
  point =  list(filter(lambda x: Xstatus.get(x[0]) == 0, [(index,prob) for index, prob in sorted(enumerate(sum(y1.tolist()[0], [])), key=lambda x:x[1]*-1)] ) )[0]
  p, _ = point
  y = p//4
  x = p%4 
  X[y][x] = 1

  y1p = (y,x)
  y1X = copy.copy(X)
  # eval and update playter2
  X = ocero_detection.update(X, y, x, type=1)
  #[print(x) for x in X]
  # この時の、1, -1の数
  size_1_1 = len(list(filter(lambda x:x==1, sum(X, []))))
  size_1_2 = len(list(filter(lambda x:x==-1, sum(X, []))))

  y, x = y1p
  y1[0][y][x] = y1[0][y][x]*(size_1_1 - size_2_1)
  player1.fit( np.array([y1X]), y1 )
  if size_1_2 < size_2_2:
    try:
      # y2を弱化する
      y, x = y2p
      y2[0][y][x] = y2[0][y][x]*0.5
      #player2.fit( np.array([y2X]), y2 )
    except NameError as ex:
      ...
  else:
    # y2を強化する
    try:
      # y2を弱化する
      y, x = y2p
      y2[0][y][x] = y2[0][y][x]*2.0
      #player2.fit( np.array([y2X]), y2 )
    except NameError as ex:
      ...

  #y2 = player2.predict( np.array([X]) )
  y2 = np.random.random_sample((1, 4, 4))
  Xstatus = {index:x for index, x in enumerate(sum(X, []))}
  point =  list(filter(lambda x: Xstatus.get(x[0]) == 0, [(index,prob) for index, prob in sorted(enumerate(sum(y2.tolist()[0], [])), key=lambda x:x[1]*-1)] ) )[0]
  p, _ = point
  y = p//4
  x = p%4 
  X[y][x] = -1

  y2p = (y,x)
  y2X = copy.copy(X)
  # eval and update player1
  X = ocero_detection.update(X, y, x, type=-1)
  #[print(x) for x in X]
  size_2_1 = len(list(filter(lambda x:x==1, sum(X, []))))
  size_2_2 = len(list(filter(lambda x:x==-1, sum(X, []))))
  if size_2_1 < size_1_1:
    #print('decline playter1')
    # y1を弱化する
    y, x = y1p
    y1[0][y][x] = y1[0][y][x]*0.5
    player1.fit( np.array([y1X]), y1 )
  else:
    # y1を強化する
    y, x = y1p
    y1[0][y][x] = y1[0][y][x]*2.0
    player1.fit( np.array([y1X]), y1 )
    
  #print('-'*10)

