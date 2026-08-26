import numpy as np
import matplotlib.pyplot as plt

N=1290
NA=600
templist=["0.23", "0.30"]

for temp in templist:
  
  if (temp == "0.23") : NT = 8
  else : NT = 6
  
  # first load propensities and positions
  data_x=np.zeros( (N) )
  data_y=np.zeros( (N) )
  data_disp=np.zeros( (NT,N) )
  data_bb=np.zeros( (NT,N) )
  
  data=np.load("../KA2D_models/T{}/train/N1290T{}_141.npz".format(temp,temp))
  data_disp[:]= data['md_prop']
  data_bb[:]= data['bb_prop']
  data_x[:]= data['initial_positions'][:,0]
  data_y[:]= data['initial_positions'][:,1]
 
  fig, ax = plt.subplots()
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  im=ax.scatter(data_x,data_y, c=data_disp[NT-1,:], cmap='coolwarm')
  fig.savefig("conf_prop_disp_T{}.png".format(temp), bbox_inches='tight')
  plt.clf()
      
  fig, ax = plt.subplots()
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  im=ax.scatter(data_x,data_y, c=data_bb[NT-1,:], cmap='coolwarm_r')
  fig.savefig("conf_prop_bb_T{}.png".format(temp), bbox_inches='tight')
  plt.clf()



# Test    
data=np.load("../KA2D_models/T{}/train/N1290T{}_99.npz".format(temp,temp))
print(data['initial_positions'])
print(data['initial_positions_inherent'])
print(data['initial_positions_cage'])
