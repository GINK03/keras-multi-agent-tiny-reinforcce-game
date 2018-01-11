import numpy as np
def update(X, y, x, type=1):
  W,H = np.array(X).shape 
  #print(W,H)
  #print(X)

  # scan to right
  buff = []
  for i in range(x+1, W):
    scan = X[y][i]
    if scan == 0:
      break
    if scan == type:
      # 反転させる
      for b in buff:
        y, i = b
        X[y][i] = type
      break
    buff.append( (y,i) )
    #print(scan)
  
  # scan to left
  buff = []
  for i in reversed(range(0, x)):
    scan = X[y][i]
    if scan == 0:
      break
    if scan == type:
      # 反転させる
      for b in buff:
        y, i = b
        X[y][i] = type
      break
    buff.append( (y,i) )
    #print(scan)
 
  # scan to duttom
  buff = []
  for i in range(y+1, H):
    scan = X[i][x]
    if scan == 0:
      break
    if scan == type:
      # 反転させる
      for b in buff:
        i, x = b
        X[i][x] = type
      break
    buff.append( (i, x) )
    #print(scan)
  
  # scan to top
  buff = []
  for i in reversed(range(0, y)):
    scan = X[i][x]
    if scan == 0:
      break
    if scan == type:
      # 反転させる
      for b in buff:
        i, x = b
        X[i][x] = type
      break
    buff.append( (i, x) )
    #print(scan)
  return X
