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

inputs_1    = Input( shape=(21,) ) 
inputs_2    = Input( shape=(3,) ) 
inputs      = Concatenate(axis=-1)( [inputs_1, inputs_2] )
x           = Dense(4000, activation='relu')( inputs )
x           = Dense(4000, activation='relu')( x )
x           = Dense(1, activation='linear')( x )
player      = Model([inputs_1, inputs_2], x )
player.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 
optimizers = [SGD(), Adam(), RMSprop()]

inputs_1    = Input( shape=(21,) ) 
inputs_2    = Input( shape=(3,) ) 
inputs      = Concatenate(axis=-1)( [inputs_1, inputs_2] )
x           = Dense(4000, activation='relu')( inputs )
x           = Dense(4000, activation='relu')( x )
x           = Dense(1, activation='sigmoid')( x )
enemy       = Model( [inputs_1, inputs_2], x )
enemy.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 

index_stat = {}
for i in range(21):
  b = [0.0]*21
  b[i] = 1.0
  index_stat[i] = b 

PATTERN = [ [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0] ]
def schedule(i):
  if   1000 > i:
    return 0.4
  elif 2000 > i:
    return 0.3
  elif 3000 > i:
    return 0.25
  else:
    return 0.25

def reinforce():
  # play game
  if '--resume' in sys.argv:
    model = sorted(glob.glob('models/player_*.h5')).pop()
    player.load_weights(model)
    model = sorted(glob.glob('models/enemy_*.h5')).pop()
    enemy.load_weights(model)
  
  result = open('result.txt', 'w')
  for i in range(300000):
    lanes_player = []
    lanes_enemy = []
    now = 0
    while True:
      next_stat_player = index_stat[now]
      if random.random() > 0.1:
        qs = [ (player.predict( [ np.array( [ next_stat_player ] ), np.array( [ xs ] ) ] ).tolist()[0][0], e) for e, xs in enumerate(PATTERN) ]
        q  = max(qs, key=lambda x:x[0])
        p  = q[1]
        print( q )
        print( qs )
      else:
        p = random.choice([0,1,2])
      lanes_player.append( (p, next_stat_player) )
      w = p + 1
      now += w
      if now >= 21:
        score = -1
        break
      
      # mode enemy
      next_stat_enemy = index_stat[now]
      if random.random() > 0.1:
        qs = [ (enemy.predict( [ np.array( [ next_stat_enemy ] ), np.array( [ xs ] ) ] ).tolist()[0][0], e) for e, xs in enumerate(PATTERN) ]
        q  = max(qs, key=lambda x:x[0])
        p  = q[1]
        print( q )
        print( qs )
      else:
        p = random.choice([0,1,2])
      lanes_enemy.append( (p, next_stat_enemy) )
      w = p + 1
      now += w
      if now >= 21:
        score = 1
        break

    result.write('%09d %d\n'%(i, score))
    print( '%09d %d'%(i, score))

    # Player
    x1s, x2s = [], []
    for p, x1 in lanes_player:
      x2    = [0.0]*3
      x2[p] = 1.0
      x1s.append( x1 )
      x2s.append( x2 )
    x2s = np.array( x2s ) 
    player.fit( [np.array(x1s), x2s], np.array( [score/len(x1s)]*len(x1s) ) , epochs=2  )
    
    # Enemy
    x1s, x2s = [], []
    for p, x1 in lanes_enemy:
      x2    = [0.0]*3
      x2[p] = 1.0
      x1s.append( x1 )
      x2s.append( x2 )
    x2s = np.array( x2s ) 
    enemy.fit( [np.array(x1s), x2s], np.array( [(score * -1)/len(x1s)]*len(x1s) ) , epochs=2  )

    if i%1000 == 0:
      player.save_weights('models/player_%09d.h5'%i)
      enemy.save_weights('models/enemy_%09d.h5'%i)

def play():
  model = sorted(glob.glob('models/player_*.h5')).pop()
  print( model )
  player.load_weights( sorted(glob.glob('models/player_*.h5')).pop() )
  now = 0
  #cursol_buff = []
  while True:
    next_stat_player = index_stat[now]
    qs = [ (player.predict( [ np.array( [ next_stat_player ] ), np.array( [ xs ] ) ] ).tolist()[0][0], e) for e, xs in enumerate(PATTERN) ]
    q  = max(qs, key=lambda x:x[0])
    p  = q[1]
    w  = p + 1
    print('コンピュータは{}を選択しました'.format(w))
    now += w
    if now >= 21:
      result = 'You win!'
      break
    print('now position', now )
    print('数字（１−３）を入力してください')
    now += int( input() )
    if now >= 21:
      result = 'あなたの負け'
      break
  print('結果', result)
  
if __name__ == '__main__':
  if '--reinforce' in sys.argv:
     reinforce()

  if '--play' in sys.argv:
    play()
