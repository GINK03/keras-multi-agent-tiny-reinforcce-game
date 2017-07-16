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
import numpy as np
import random
import sys
import glob
import pickle
import re

inputs      = Input( shape=(21,) ) 
x           = Dense(4000, activation='relu')( inputs )
x           = Dense(4000, activation='relu')( x )
x           = Dense(3, activation='tanh')( x )
player      = Model( inputs, x )
player.compile( optimizer=Adam(), loss='mse', metrics=['accuracy'] ) 
optimizers = [SGD(), Adam(), RMSprop()]

inputs      = Input( shape=(21,) ) 
x           = Dense(4000, activation='relu')( inputs )
x           = Dense(4000, activation='relu')( x )
x           = Dense(3, activation='tanh')( x )
enemy       = Model( inputs, x )
enemy.compile( optimizer=SGD(lr=0.2), loss='mse', metrics=['accuracy'] ) 

optimizers_enemy = [SGD(lr=0.2),SGD(lr=0.09),  Adam(lr=0.01), Adam(lr=0.05), Adam(), RMSprop()]
index_stat = {}
for i in range(21):
  b = [0.0]*21
  b[i] = 1.0
  index_stat[i] = b 

def schedule(i):
  if   1000 > i:
    return 0.4
  elif 2000 > i:
    return 0.3
  elif 3000 > i:
    return 0.25
  else:
    return 0.25

SCORE_BOARD = [-1, -1]
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
        p = np.argmax( player.predict( np.array( [ next_stat_player ] ) ) )
      else:
        p = random.choice([0,1,2])
      lanes_player.append( (p, next_stat_player) )
      w = p + 1
      now += w
      if now == 20:
        score = 1
        break
      elif now > 20:
        score = -1
        break
      # another way
      next_stat_enemy = index_stat[now]
      if random.random() > schedule(i):
        e = np.argmax( enemy.predict( np.array( [ next_stat_enemy ] ) ) )
      else:
        e = random.choice([0,1,2])
      lanes_enemy.append( (e, next_stat_enemy) )
      now += e + 1
      if now == 20:
        score = -1
        break
      elif now > 20:
        score = 1
        break
    res =  '%09d score %d\n'%(i, score)
    result.write(res)
    SCORE_BOARD.append( score )
    print(res, end='')
    # Player
    ys, xs = [], []
    for p, x in lanes_player:
      y    = [0.0]*3
      y[p] = 1.0
      xs.append( x )
      ys.append( y )
    ys = np.array( ys ) * score
    optim = random.choice( optimizers )
    player.otimizer = optim
    player.fit(np.array(xs), ys, epochs=2  )

    # Enemy
    ys, xs = [], []
    for e, x in lanes_enemy:
      y    = [0.0]*3
      y[e] = 1.0
      xs.append( x )
      ys.append( y )
    enemy_score = -1*score
    ys = np.array( ys ) * enemy_score
    optim = random.choice( optimizers_enemy )
    enemy.otimizer = optim
    enemy.fit(np.array(xs), ys, epochs=2  )
    if i%2000 == 0:
      player.save_weights('models/player_%09d.h5'%i)
      enemy.save_weights('models/enemy_%09d.h5'%i)

def play():
  model = sorted(glob.glob('models/player_*.h5')).pop()
  print( model )
  player.load_weights( sorted(glob.glob('models/player_*.h5')).pop() )
  now = 0
  #cursol_buff = []
  while True:
    next_stat = index_stat[now]
    p = np.argmax( player.predict( np.array( [ next_stat ] ) ) )
    w = p + 1
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
