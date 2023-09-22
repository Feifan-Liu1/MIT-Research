import h5py
import numpy as np
import matplotlib.pyplot as plt
f = h5py.File('trees_sf1_091.0.hdf5','r')
# tree = f['Tree88938']
# SubhaloPos = tree['SubhaloPos']
# print(np.size(SubhaloPos))
# pos = np.array(SubhaloPos)
# x = pos[:,0]
# y = pos[:,1]
# z = pos[:,2]

# # 2D plot for x and y axes
# # plt.plot(x, y, ls='', marker=',')
# # plt.show()

# # 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(projection = '3d')
# ax.scatter(x, y, z, marker=',', s = plt.rcParams['lines.markersize']/10)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()

tree = f['Tree100']
SubhaloPos = tree['SubhaloPos']
Descendant = tree['Descendant']
FirstProgenitor = tree['FirstProgenitor']
SubhaloBHMass = tree['SubhaloBHMass']
pos = np.array(SubhaloPos)
des = np.array(Descendant)
pro = np.array(FirstProgenitor)
mass = np.array(SubhaloBHMass)
print(mass)
x = pos[:,0]
y = pos[:,1]
z = pos[:,2]

plt.scatter(x,y,s = plt.rcParams['lines.markersize']/10**2)
plt.xlabel('X')
plt.ylabel('Y')
# fig = plt.figure()
# ax = fig.add_subplot(projection = '2d')
# ax.scatter(x, y, z, marker=',', s = plt.rcParams['lines.markersize']/10**3)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# des = pro
for i in range(np.size(des)):
    if des[i]!=-1:
        des_i = des[i]
        des_pos = pos[des_i]
        des_x = des_pos[0]
        des_y = des_pos[1]
        des_z = des_pos[2]
        x_pair = np.array([x[i],des_x])
        y_pair = np.array([y[i],des_y])
        # z_pair = np.array([z[i],des_z])
        # ax.plot(x_pair, y_pair, z_pair, color = 'red', linewidth=0.05 )
        plt.plot(x_pair, y_pair, color = 'red', linewidth=0.1 )

plt.show()