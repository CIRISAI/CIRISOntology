import numpy as np
import matplotlib.pyplot as plt

# load first structure of the test dataset for the longest time scale
data=np.load("./T0.23/test/N1290T0.23_151_tc40.npz")
#print (data['positions'], data['initial_positions'])

# calculate isoconfigurational average of displacement for each particle
displacement = data['positions'] - data['initial_positions']
boxL = data['box']
for x in range(displacement.shape[0]):
    displacement[x]=np.where(displacement[x] > boxL/2.0, displacement[x] - boxL, displacement[x])
    displacement[x]=np.where(displacement[x] < -boxL/2.0, displacement[x] + boxL, displacement[x])
sq_displacement = np.sqrt(displacement[:,:,0]*displacement[:,:,0] + displacement[:,:,1]*displacement[:,:,1])
sq_displacement = np.mean(sq_displacement,axis=0)

# print isoconfigurational average
print(sq_displacement)

initial_positions = data['initial_positions']
initial_positions=np.where(initial_positions < - boxL/2.0, initial_positions + boxL, initial_positions)
initial_positions=np.where(initial_positions < - boxL/2.0, initial_positions + boxL, initial_positions)
initial_positions=np.where(initial_positions > boxL/2.0, initial_positions - boxL, initial_positions)
initial_positions=np.where(initial_positions > boxL/2.0, initial_positions - boxL, initial_positions)

fig, ax = plt.subplots()
ax.set_xlabel("X")
ax.set_ylabel("Y")
im=ax.scatter(initial_positions[:,0],initial_positions[:,1], c=sq_displacement, cmap='coolwarm')
fig.savefig("conf_prop_disp_T0.23.png", bbox_inches='tight')
plt.clf()