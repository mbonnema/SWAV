#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 13:35:22 2021

@author: mbonnema
"""

#from ReadJRC_batch import ReadJRC
#from ReadS1_csv import ReadS1
from ReadJRC_batch import ReadJRC
from ReadS1_batch import ReadS1
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import csv

#S1dir = '../../Results/World_Ver2/'
#JRCdir = '../../Results/JRC_100_1000/'
#S1dir = '../../Results/SWAV_10_100/'
#JRCdir = '../../Results/JRC_10_100/'
S1dir = '../../Results/S1_1_10/'
JRCdir = '../../Results/JRC_1_10_2/'

S1_d, S1_A, S1_WE, S1_LE = ReadS1(S1dir)
JRC_d, JRC_A, JRC_ND = ReadJRC(JRCdir)

CorS1A = []
CorJRCA = []
CorID = []
for ID in S1_d:
    s1d = S1_d[ID]
    s1a = S1_A[ID]
    s1we = S1_WE[ID]
    s1le = S1_LE[ID]
    
    try:
        jrcd = JRC_d[ID]
        jrca = JRC_A[ID]
        jrcnd = JRC_ND[ID]
    except:
        #print('Error at ID: '+ID)
        continue
    
    for d,a,we,le in zip(s1d,s1a,s1we,s1le):
        if d in jrcd:
            I = jrcd.index(d)
        else:
            continue
        ja = jrca[I]
        jnd = jrcnd[I]
        if we < 0:
            we = 0
        if le < 0:
            le = 0
        if jnd > 0.01:
            continue
        if a == 0:
            continue
        if we/a > 0.1 or le/a > 0.1:
            continue
        CorS1A.append(a)
        CorJRCA.append(ja)
        CorID.append(ID)
        
'''
for s1, jrc, ID in zip(CorS1A,CorJRCA,CorID):
    if jrc > 800 and s1 < 600:
        print('ID = ' + str(ID) + ' S1 = ' + repr(s1) + ' JRC = ' + repr(jrc))
'''        
corAJRCar = np.array(CorJRCA).reshape((-1, 1))
corAS1ar = np.array(CorS1A)



model = LinearRegression(fit_intercept=True).fit(corAJRCar, corAS1ar)
r_sq = model.score(corAJRCar, corAS1ar)
intercept = model.intercept_
coefficient = model.coef_[0]
linFit_x = np.array(range(0,20,1))
linFit_y = linFit_x
#linFit_y = linFit_x*coefficient + intercept
print('m = ' + repr(coefficient))
print('b = ' + repr(intercept))
print('r_sq = ' + repr(r_sq))


heatmap, xedges, yedges = np.histogram2d(CorJRCA, CorS1A, bins=300)
heatmap[heatmap == 0] = 0.1
heatmap = np.log(heatmap)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
plt.figure(figsize=(10,10))
plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.plot(linFit_x,linFit_y,linestyle = '-',c='black')

'''     
plt.figure(figsize=(10,10))
plt.scatter(CorJRCA,CorS1A, s=2, alpha=0.4)
'''
plt.gca().set_aspect('equal', 'box')
plt.gca().set(xlim=(0, 15), ylim=(0, 15))
plt.gca().set_xlabel('Water Surface Area from JRC $\mathregular{km^{2}}$', fontsize = 16)
plt.gca().set_ylabel('Water Surface Area from S1 $\mathregular{km^{2}}$', fontsize = 16)
plt.show()


S1_area = open('../../Results/S1_Area.csv','w')
S1_writer = csv.writer(S1_area)
JRC_area = open('../../Results/JRC_Area.csv','w')
JRC_writer = csv.writer(JRC_area)

for s1a, jrca in zip(CorS1A,CorJRCA):
    S1_writer.writerow([s1a])
    JRC_writer.writerow([jrca])
    
S1_area.close()
JRC_area.close()
