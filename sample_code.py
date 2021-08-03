import numpy as np
import matplotlib.pyplot as plt
import math as m

def iterate(tau,Z,x,t,b): #iterates map up to next t_z, t_h, or t_d
    
    s = t % 1 
    sign = 1 if s < 1/2 else -1 # current sign of the forcing term
    forcing = b*np.copysign(1.0, sign)
    feedback = m.copysign(1.0,x)*(-1)**(len(Z)+1)
    drive = feedback + forcing
    
    t_d = (0.5) -  (t % (0.5)) # time until the next change in forcing
    t_h = tau + Z[0] if len(Z) > 0 else np.infty # time until the next change of feedback
    t_z = -x/drive if -x/drive > 0 else np.infty # time until the next zero crossing
    t = min([t_d,t_h,t_z])
    at = np.argmin([t_d,t_h,t_z])
    
    for i in range(0, len(Z)):
        Z[i] = Z[i] - t
        
    xnew = x + t*drive if at != 2  else m.copysign(0,-x) # maintains the correct direction when the trajectory hits x=0
    
    if at == 2: # zero crossing
        Z.append(0.0)
        
    if at == 1: # feedback changed due zero crossing tau time ago
        del Z[0]
        
            
    return xnew,t

def simulate(tau,Z,x,tmax,b):#iterates the map up to time tmax
    
    T = [0]
    X = [x]
    H = [[]]
    
    while T[-1] < tmax:
        x,t = iterate(tau,Z,x,T[-1],b)
        tnew = T[-1] + t
        T.append(tnew)
        X.append(x)
        H.append(Z[:])
    return X[:],T[:],H[:] # position, time, history

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 20})
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(111)

tau,b,hist,x0 = 0.95, 1.35, [-0.94], 0.01 # paramaters and initial conditions
tmax = 1000

X,T,H= simulate(tau,hist,x0,tmax,b) # burn in simulation
X,T,H= simulate(tau,H[-1],X[-1],10,b) # data to be plotted

for j in range(0,10):
    ax1.axvline(j, color = 'k', linestyle='--',lw=1)
    ax1.axvline(j+0.5, color = 'k' ,linestyle='--',lw=1)
ax1.axhline(0,color = 'k',lw=1)
ax1.plot(T,X,c='b',lw = 1.5,label = "x(t)")
ax1.set_xlim(0,10)
y = 1.25
ax1.set_ylim(-y,y)
    
ax1.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
ax1.set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
ax1.set_xlabel(r'$t$',fontsize=24)
ax1.set_ylabel(r'$x(t)$',fontsize=24)
    
plt.savefig('sample_solution.pdf')