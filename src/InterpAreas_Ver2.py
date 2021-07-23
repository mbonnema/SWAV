#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:04:11 2020

@author: mbonnema
"""

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
from datetime import timedelta

import ee
ee.Initialize()

def InterpolateAreas(Dir,IDList):
    smoothFlag = 1
    #lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
    #largeLakes = lakes.filter(ee.Filter.inList('system:index',IDList))
        
    #lakeID = largeLakes.aggregate_array('system:index').getInfo()
    #lakeArea = largeLakes.aggregate_array('Lake_area').getInfo()
    
    
    files = os.listdir(Dir)
    def getTxt(f):
        if (f[-4:] == '.txt'):
            return True
        else:
            return False
    files = list(filter(getTxt,files))
    
    ListofDateLists = []
    ListofAreaLists = []
    ListofWErLists = []
    ListofLErLists = []
    masterDates = []
    ListofIDs = []
    
    for file in files:
        ID = file[:-4]
        if ID not in IDList:
            continue
        Data = open(Dir+file,'r')
        
        Lines = Data.readlines()
        Lines.pop(0)
        
        Area = []
        WEr = []
        LEr = []
        Date = []
        CountGood = 0
        CountBad = 0
        for line in Lines:
           try:
               line = line.split('\t')
               date = int(line[0])
               #date = datetime.datetime.fromtimestamp(date/1000)
               area = float(line[1])
               wMean = float(line[2])
               wStd = float(line[3])
               lMean = float(line[4])
               lStd = float(line[5])
               WProb = int(line[6])
               wError = float(line[8])
               lError = float(line[9][:-1])
               if date in Date:
                   continue
               if wError > 10000 or lError > 10000:
                   continue
               if wError < 0:
                   wError = 0
               if lError < 0:
                   lError = 0
               if wError/area > 0.1 or lError/area > 0.1:
                   continue
               Area.append(area)
               WEr.append(wError)
               LEr.append(lError)
               Date.append(date)
               CountGood = CountGood + 1
           except Exception as e:
               print(str(e))
        
        if WProb < 0:
            #print(ID+" Skipped due to WProb<95"+" Actual WProb =" + str(WProb))
            continue
        
        masterDates.extend(Date)
        masterDates = list(set(masterDates))
        masterDates.sort()
        
        ListofDateLists.append(Date)
        ListofAreaLists.append(Area)
        ListofWErLists.append(WEr)
        ListofLErLists.append(LEr)
        
        ListofIDs.append(ID)
    hardcodeDates = [datetime.datetime(2017, 1, 1, 16, 0), datetime.datetime(2017, 2, 1, 16, 0), datetime.datetime(2017, 3, 1, 16, 0), datetime.datetime(2017, 4, 1, 17, 0), datetime.datetime(2017, 5, 1, 17, 0), datetime.datetime(2017, 6, 1, 17, 0), datetime.datetime(2017, 7, 1, 17, 0), datetime.datetime(2017, 8, 1, 17, 0), datetime.datetime(2017, 9, 1, 17, 0), datetime.datetime(2017, 10, 1, 17, 0), datetime.datetime(2017, 11, 1, 17, 0), datetime.datetime(2017, 12, 1, 16, 0), datetime.datetime(2018, 1, 1, 16, 0), datetime.datetime(2018, 2, 1, 16, 0), datetime.datetime(2018, 3, 1, 16, 0), datetime.datetime(2018, 4, 1, 17, 0), datetime.datetime(2018, 5, 1, 17, 0), datetime.datetime(2018, 6, 1, 17, 0), datetime.datetime(2018, 7, 1, 17, 0), datetime.datetime(2018, 8, 1, 17, 0), datetime.datetime(2018, 9, 1, 17, 0), datetime.datetime(2018, 10, 1, 17, 0), datetime.datetime(2018, 11, 1, 17, 0), datetime.datetime(2018, 12, 1, 16, 0), datetime.datetime(2019, 1, 1, 16, 0), datetime.datetime(2019, 2, 1, 16, 0), datetime.datetime(2019, 3, 1, 16, 0), datetime.datetime(2019, 4, 1, 17, 0), datetime.datetime(2019, 5, 1, 17, 0), datetime.datetime(2019, 6, 1, 17, 0), datetime.datetime(2019, 7, 1, 17, 0), datetime.datetime(2019, 8, 1, 17, 0), datetime.datetime(2019, 9, 1, 17, 0), datetime.datetime(2019, 10, 1, 17, 0), datetime.datetime(2019, 11, 1, 17, 0), datetime.datetime(2019, 12, 1, 16, 0), datetime.datetime(2020, 1, 1, 16, 0)]
    masterDates = []
    for d in hardcodeDates:
        d = int(datetime.datetime.timestamp(d - timedelta(days=1))*1000)
        masterDates.append(d)
    
    formatDates = []
    for d in masterDates:
        formatDates.append(datetime.datetime.fromtimestamp(d/1000) + timedelta(days=1))
    
    masterAreas = []
    masterWEr = []
    masterLEr = []
    masterID = []
    i = -1
    for A, D, WE, LE, ID in zip(ListofAreaLists, ListofDateLists, ListofWErLists, ListofLErLists, ListofIDs):
        i = i+1
        consec_interp = 0
        interpFlag = 0
        Acomplete = []
        WEcomplete = []
        LEcomplete = []
        try:
            for d in masterDates:
                if d in D:
                    I = D.index(d)
                    Acomplete.append(A[I])
                    WEcomplete.append(WE[I])
                    LEcomplete.append(LE[I])
                    consec_interp = 0
                else:
                    consec_interp = consec_interp+1
                    if consec_interp > 4:
                        interpFlag = 1
                    Dlst = np.asarray(D)
                    id1 = (np.abs(Dlst-d)).argmin()
                    d1 = Dlst[id1]
                    a1 = A[id1]
                    we1 = WE[id1]
                    le1 = LE[id1]
                    
                    Dlst = list(Dlst)
                    Dlst.remove(d1)
                    Dlst = np.asarray(Dlst)
                    Alst = list(np.asarray(A))
                    Alst.remove(a1)
                    WElst = list(np.asarray(WE))
                    WElst.remove(we1)
                    LElst = list(np.asarray(LE))
                    LElst.remove(le1)
                    
                    id2 = (np.abs(Dlst-d)).argmin()
                    d2 = Dlst[id2]
                    a2 = Alst[id2]
                    we2 = WElst[id2]
                    le2 = LElst[id2]
                    
                    a = a1 + (d-d1)*(a2-a1)/(d2-d1)
                    we = we1 + (d-d1)*(we2-we1)/(d2-d1)
                    le = le1 + (d-d1)*(le2-le1)/(d2-d1)
                    Acomplete.append(a)
                    WEcomplete.append(we)
                    LEcomplete.append(le)
            if interpFlag == 0:  
                if smoothFlag == 1:
                    smoothedA = []
                    smoothedWE = []
                    smoothedLE = []
                    for I, a in enumerate(Acomplete):
                        if I == 0:
                            sa = np.mean([a,Acomplete[I+1]])
                        elif I == len(Acomplete)-1:
                            sa = np.mean([a,Acomplete[I-1]])
                        else:
                            sa = np.mean([a,Acomplete[I-1],Acomplete[I+1]])
                        smoothedA.append(sa)
                    Acomplete = smoothedA
                    for I, we in enumerate(WEcomplete):
                        if I == 0:
                            sa = np.median([we,WEcomplete[I+1]])
                        elif I == len(WEcomplete)-1:
                            sa = np.median([we,WEcomplete[I-1]])
                        else:
                            sa = np.median([we,WEcomplete[I-1],WEcomplete[I+1]])
                        smoothedWE.append(sa)
                    WEcomplete = smoothedWE
                    for I, le in enumerate(LEcomplete):
                        if I == 0:
                            sa = np.median([le,LEcomplete[I+1]])
                        elif I == len(LEcomplete)-1:
                            sa = np.median([le,LEcomplete[I-1]])
                        else:
                            sa = np.median([le,LEcomplete[I-1],LEcomplete[I+1]])
                        smoothedLE.append(sa)
                    LEcomplete = smoothedLE
                masterAreas.append(Acomplete)
                masterWEr.append(WEcomplete)
                masterLEr.append(LEcomplete)
                masterID.append(ID)
                
            else:
                pass
                #print('Element:'+str(i)+"\tskipped due to too many consecutive interpolations")
        except Exception as e:
            pass
            #print('Error at element: '+str(i)+"\t"+str(e))
    
    masterAreas = np.array(masterAreas)
    masterWEr = np.array(masterWEr)
    masterLEr = np.array(masterLEr)
    #sumAreas = np.sum(masterAreas,axis=0)
    Dates = formatDates
    #Dates = mdates.date2num(formatDates)
    
    '''
    SuccessArea = 0
    for ID in masterID:
        I = lakeID.index(ID)
        nomArea = float(lakeArea[I])
        SuccessArea = SuccessArea + nomArea
    
    FailArea = 0
    for ID in IDList:
        if ID in masterID:
            continue
        else:
            I = lakeID.index(ID)
            nomArea = float(lakeArea[I])
            FailArea = FailArea + nomArea
    '''        
    '''
    print('*****************************************************************')
    print('Aggregation Complete')
    print('Total: '+ str(len(IDList)) + '\tSuccess: '+ str(len(masterID)) + '\tFailure: ' + str(len(masterID)-len(IDList)))
    print('Total Water Body Area: '+str(SuccessArea+FailArea)+ 'km^2')
    print('Area of Water Bodies Succesfully Captured: '+str(SuccessArea) + 'km^2')
    print('Areaof WaterBodies Missed: ' + str(FailArea) + 'km^2')
    '''
    return masterID, Dates, masterAreas, masterWEr, masterLEr
                

                
            
        
        