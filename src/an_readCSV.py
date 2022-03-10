#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 09:18:16 2022

@author: mbonnema
"""
import datetime

def readCSV(folderPath):
    areaFile = folderPath + 'SurfaceArea.csv'
    lerrorFile = folderPath + 'Lerror.csv'
    werrorFile = folderPath + 'Werror.csv'
    nodataFile = folderPath + 'Nodata.csv'
    
    D = {}
    A = {}
    LE = {}
    WE = {}
    ND = {}
    DatesList = []
    
    f = open(areaFile,'r')
    lines = f.readlines()
    dates = lines[0].strip('\n').split(',')[1:]
    for d in dates:
        d = d.split('/')
        month = int(d[1])
        year = int(d[0])
        day = int(d[2])
        hour = int(d[3])
        DatesList.append(datetime.datetime(year, month, day, hour, 0))
    
    lines = lines[1:]
    line = lines[0]
    for line in lines:
        line = line.split(',')
        ID = line[0]
        line = line[1:]
        areas = []
        adates = []
        for item,a_d in zip(line,DatesList):
            a = float(item)
            if a > -9999:
                areas.append(a)
                adates.append(int(datetime.datetime.timestamp(a_d)*1000))
        A[ID] = areas
        D[ID] = adates
    f.close()
    #print(D['1646']) 
    f = open(lerrorFile,'r')
    lines = f.readlines()
    lines = lines[1:]
    line = lines[0]
    for line in lines:
        line = line.split(',')
        ID = line[0]
        line = line[1:]
        lerrors = []
        for item,a_d in zip(line,DatesList):
            le = float(item)
            if le > -9999:
                lerrors.append(le)
        LE[ID] = lerrors
    f.close()  
    
    f = open(werrorFile,'r')
    lines = f.readlines()
    lines = lines[1:]
    line = lines[0]
    for line in lines:
        line = line.split(',')
        ID = line[0]
        line = line[1:]
        werrors = []
        for item,a_d in zip(line,DatesList):
            we = float(item)
            if we > -9999:
                werrors.append(we)
        WE[ID] = werrors
    f.close()
    
    f = open(nodataFile,'r')
    lines = f.readlines()
    lines = lines[1:]
    line = lines[0]
    for line in lines:
        line = line.split(',')
        ID = line[0]
        line = line[1:]
        nodata = []
        for item,a_d in zip(line,DatesList):
            nd = float(item)
            if nd > -9999:
                nodata.append(nd)
        ND[ID] = nodata
    f.close()
    
    return D,A,LE,WE,ND
    
#readCSV('../../Results/World_Ver3_CSV/')