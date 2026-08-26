import numpy as np
import matplotlib.pyplot as plt

NTest=100
N=4096
NA=3277
NT=10
TSTART=1
templist=["0.44", "0.50", "0.56", "0.64"]

# first load propensities and positions
data_x=np.zeros( (len(templist),N) )
data_y=np.zeros( (len(templist),N) )
data_z=np.zeros( (len(templist),N) )
data_disp=np.zeros( (len(templist),NT,N) )
data_bb=np.zeros( (len(templist),NT,N) )

counttemp=0
for temp in templist:
  data=np.load("../KA_models/T{}/train/N4096T{}_301.npz".format(temp,temp))
  data_disp[counttemp,:]= data['md_prop']
  data_bb[counttemp,:]= data['bb_prop']
  data_x[counttemp,:]= data['initial_positions'][:,0]
  data_y[counttemp,:]= data['initial_positions'][:,1]
  data_z[counttemp,:]= data['initial_positions'][:,2]
  counttemp += 1

counttemp=0  
for temp in templist:  
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_ylabel("Z")
  im=ax.scatter(data_x[counttemp],data_y[counttemp],data_z[counttemp], c=data_disp[counttemp,6,:], cmap='coolwarm')
  fig.savefig("conf_prop_disp_T{}.png".format(temp), bbox_inches='tight')
  plt.clf()
      
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_ylabel("Z")
  im=ax.scatter(data_x[counttemp],data_y[counttemp],data_z[counttemp], c=data_bb[counttemp,6,:], cmap='coolwarm_r')
  fig.savefig("conf_prop_bb_T{}.png".format(temp), bbox_inches='tight')
  plt.clf()
  counttemp += 1


# Test    
data=np.load("../KA_models/T{}/train/N4096T{}_99.npz".format(0.44,0.44))
print(data['initial_positions'])
print(data['initial_positions_inherent'])
print(data['initial_positions_cage'])
    

