import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import spatial

f = h5py.File('/nfs/mvogelsblab002/Users/jborrow/NewThesanRuns/Thesan/L4N512/trees_sf1_091.0.hdf5','r')

class Node:
    def __init__(self,treeIndex,des,pro,mass,snap,stars,gas,mass_re,stars_re,gas_re):
        self.treeIndex = treeIndex
        self.des = des
        self.pro = pro
        self.mass = mass
        self.snap = snap
        self.stars = stars
        self.gas = gas
        self.mass_re = mass_re
        self.stars_re = stars_re
        self.gas_re = gas_re
        


# return the array of nodes recording haloes and their information in the mergetree
def treeNodeArray(f,num):
    id = num #Treeid
    t = f['Tree%d'%id]
    des = t['Descendant']
    snap = t['SnapNum']
    idxInGroup = t['SubhaloNumber']
    des_size = np.size(des)

    SubhaloMassType = t['SubhaloMassType']
    massType = np.array(SubhaloMassType)
    mass_re = np.sum(massType, axis = 1) # prerecorded mass of halos, sum over Type
    stars_re = massType[:,4]
    gas_re = massType[:,0]

    def computeHaloMass(halo_snap,halo_idx):
        # compute mass for each subhalo
        f = h5py.File('/pool001/feifanl/subhalo_mass_snap%d.h5'%halo_snap)
        gas_total_mass = f['gas_total_mass']
        star_total_mass = f['star_total_mass']
        gas_mass = np.array(gas_total_mass)
        star_mass = np.array(star_total_mass)  
        gas = gas_mass[halo_idx]
        star = star_mass[halo_idx]
        mass = gas+star
        return mass, star, gas


    nodeArray = []
    max_91 = 0
    max_idx = 0

    snap91 = [] #record halo index and mass of snap 91
    # initialize an array of nodes
    for i in range(des_size):
        halo_snap = snap[i]
        halo_idx = idxInGroup[i]
        halo_mass,halo_star,halo_gas = computeHaloMass(halo_snap,halo_idx)

        if halo_snap == 91:
            # if halo_mass > max_91:
            #     max_91 = halo_mass
            #     max_idx = i
            snap91.append([i,halo_mass])
    
        nodeArray.append(Node(id,None,[], halo_mass,halo_snap,halo_star,halo_gas,mass_re[i],stars_re[i],gas_re[i]))

    # fill in the descendent and progenitor of the node
    for j in range(des_size):
        if des[j]!=-1:
            des_index = des[j]
            nodeArray[j].des = nodeArray[des_index]
            nodeArray[des_index].pro.append(nodeArray[j])
    return nodeArray, snap91

# plot the main proganitor (halor with the max mass in each snapshot) tree, mass vs snapshot
def plotMainPro(current_node):
    if current_node.pro==[]:
        return
    else:
        current_y = current_node.mass
        current_x = current_node.snap
        # current_y_re = current_node.mass_re

        pro_mass = np.empty(0)
        # pro_mass_re = np.empty(0)
        for j in range(len(current_node.pro)):
            pro_node = current_node.pro[j] 
            pro_mass = np.append(pro_mass,pro_node.mass)
            # pro_mass_re = np.append(pro_mass_re,pro_node.mass_re)
        
        max_idx = np.argmax(pro_mass)
        main_node = current_node.pro[max_idx] 

        pro_y = main_node.mass
        pro_x = main_node.snap
        plt.plot([current_x, pro_x],[np.log(current_y),np.log(pro_y)],c = 'orange',zorder=1)
        plt.scatter(current_x, np.log(current_y),c = "orange",s = 5, zorder=2)
        plt.scatter(pro_x, np.log(pro_y),c = "orange",s = 5, zorder=2)

        # max_idx_re = np.argmax(pro_mass_re)
        # main_node_re = current_node.pro[max_idx_re] 
        # pro_y_re = main_node_re.mass_re
        # pro_x = main_node_re.snap
        # if current_x==90 or current_x == 91:
        #     print([current_x, pro_x],[np.log(current_y_re),np.log(pro_y_re)])
        # plt.plot([current_x, pro_x],[np.log(current_y_re),np.log(pro_y_re)],c = '#1f77b4',zorder=1)
        # plt.scatter(current_x, np.log(current_y_re),c = "#1f77b4",s = 5, zorder=2)
        # plt.scatter(pro_x, np.log(pro_y_re),c = "#1f77b4",s = 5, zorder=2)


        plotMainPro(main_node)


def plotMainProRe(current_node):
    if current_node.pro==[]:
        return
    else:
        #print("current_pro", len(current_node.pro))
        current_x = current_node.snap
        #print(current_x)
        current_y_re = current_node.mass_re

        pro_mass_re = np.empty(0)
        for j in range(len(current_node.pro)):
            pro_node = current_node.pro[j] 
            pro_mass_re = np.append(pro_mass_re,pro_node.mass_re)

        max_idx_re = np.argmax(pro_mass_re)
        main_node_re = current_node.pro[max_idx_re]

        # if main_node_re.pro == []:
        #     print(pro_mass_re.shape)
        #     if len(pro_mass_re)>1:
        #         max_idx_re = np.argsort(pro_mass_re)[-2]
        #         main_node_re = current_node.pro[max_idx_re] 

        #("pro_pro", len(main_node_re.pro))
        pro_y_re = main_node_re.mass_re
        pro_x = main_node_re.snap

        plt.plot([current_x, pro_x],[np.log(current_y_re),np.log(pro_y_re)],c = '#1f77b4',zorder=1)
        plt.scatter(current_x, np.log(current_y_re),c = "#1f77b4",s = 5, zorder=2)
        plt.scatter(pro_x, np.log(pro_y_re),c = "#1f77b4",s = 5, zorder=2)


        plotMainProRe(main_node_re)

# def plotRecord(current_node):
#     if current_node.pro==[]:
#         return
#     else:
#         current_y = current_node.mass_re
#         current_x = current_node.snap

#         pro_mass = np.empty(0)
#         for j in range(len(current_node.pro)):
#             pro_node = current_node.pro[j] 
#             pro_mass = np.append(pro_mass,pro_node.mass_re)
#         max_idx = np.argmax(pro_mass)
#         main_node = current_node.pro[max_idx] 
#         pro_y = main_node.mass_re
#         pro_x = main_node.snap
#         plt.plot([current_x, pro_x],[current_y,pro_y],c = '#1f77b4',zorder=1)
#         plt.scatter(current_x, current_y,c = "#1f77b4",s = 5, zorder=2)
#         plt.scatter(pro_x, pro_y,c = "#1f77b4",s = 5, zorder=2)
#         plotRecord(pro_node)

treeNum = 0
nodeArray, snap91 = treeNodeArray(f, treeNum) 
snap91 = np.array(snap91)
idx_2nd = np.argsort(snap91[:,1])[-1]
        
current_node = nodeArray[idx_2nd]


plotMainPro(current_node)
plotMainProRe(current_node)
# plotRecord(current_node)
plt.title('Tree%d'%treeNum)
plt.xlabel("snapshot")
plt.ylabel("mass")
#plt.xticks(range(49,80))
plt.legend(loc="upper left")
plt.savefig("mass_plot.png")
#plt.show()