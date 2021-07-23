#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 19:46:38 2021

@author: mbonnema
"""

import os
import csv
import ee
import datetime
from datetime import timedelta
ee.Initialize()

S1ResultsPath = '../../Results/World_Ver2/'
lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
largeLakes = lakes.filter(ee.Filter.gt('Lake_area',100)) \
    .filter(ee.Filter.lt('Lake_area',1000))
    
lakeIndexes = largeLakes.aggregate_array('system:index').getInfo()
lakeIDs = largeLakes.aggregate_array('Hylak_id').getInfo()
files = os.listdir(S1ResultsPath)

AreaCSV = open('../../Results/World_Ver2_CSV/SurfaceArea.csv','w')
Awriter = csv.writer(AreaCSV)
WmeanCSV = open('../../Results/World_Ver2_CSV/WMean.csv','w')
WMwriter = csv.writer(WmeanCSV)
WStddevCSV = open('../../Results/World_Ver2_CSV/WStddev.csv','w')
WSwriter = csv.writer(WStddevCSV)
LmeanCSV = open('../../Results/World_Ver2_CSV/LMean.csv','w')
LMwriter = csv.writer(LmeanCSV)
LStddevCSV = open('../../Results/World_Ver2_CSV/LStddev.csv','w')
LSwriter = csv.writer(LStddevCSV)
WerrorCSV = open('../../Results/World_Ver2_CSV/Werror.csv','w')
WEwriter = csv.writer(WerrorCSV)
LerrorCSV = open('../../Results/World_Ver2_CSV/Lerror.csv','w')
LEwriter = csv.writer(LerrorCSV)
hardcodeDates = [datetime.datetime(2017, 1, 1, 16, 0), datetime.datetime(2017, 2, 1, 16, 0), datetime.datetime(2017, 3, 1, 16, 0), datetime.datetime(2017, 4, 1, 17, 0), datetime.datetime(2017, 5, 1, 17, 0), datetime.datetime(2017, 6, 1, 17, 0), datetime.datetime(2017, 7, 1, 17, 0), datetime.datetime(2017, 8, 1, 17, 0), datetime.datetime(2017, 9, 1, 17, 0), datetime.datetime(2017, 10, 1, 17, 0), datetime.datetime(2017, 11, 1, 17, 0), datetime.datetime(2017, 12, 1, 16, 0), datetime.datetime(2018, 1, 1, 16, 0), datetime.datetime(2018, 2, 1, 16, 0), datetime.datetime(2018, 3, 1, 16, 0), datetime.datetime(2018, 4, 1, 17, 0), datetime.datetime(2018, 5, 1, 17, 0), datetime.datetime(2018, 6, 1, 17, 0), datetime.datetime(2018, 7, 1, 17, 0), datetime.datetime(2018, 8, 1, 17, 0), datetime.datetime(2018, 9, 1, 17, 0), datetime.datetime(2018, 10, 1, 17, 0), datetime.datetime(2018, 11, 1, 17, 0), datetime.datetime(2018, 12, 1, 16, 0), datetime.datetime(2019, 1, 1, 16, 0), datetime.datetime(2019, 2, 1, 16, 0), datetime.datetime(2019, 3, 1, 16, 0), datetime.datetime(2019, 4, 1, 17, 0), datetime.datetime(2019, 5, 1, 17, 0), datetime.datetime(2019, 6, 1, 17, 0), datetime.datetime(2019, 7, 1, 17, 0), datetime.datetime(2019, 8, 1, 17, 0), datetime.datetime(2019, 9, 1, 17, 0), datetime.datetime(2019, 10, 1, 17, 0), datetime.datetime(2019, 11, 1, 17, 0), datetime.datetime(2019, 12, 1, 16, 0), datetime.datetime(2020, 1, 1, 16, 0)]
header = ['HyLake_ID']
for d in hardcodeDates:
    header.append(d.strftime("%m/%Y"))
Awriter.writerow(header)
WMwriter.writerow(header)
WSwriter.writerow(header)
LMwriter.writerow(header)
LSwriter.writerow(header)
WEwriter.writerow(header)
LEwriter.writerow(header)

def getTxt(f):
    if (f[-4:] == '.txt'):
        return True
    else:
        return False
files = list(filter(getTxt,files))

for f in files:
    ID = f[:-4]
    if ID not in lakeIndexes:
        continue
    else:
        hylakID = lakeIDs[lakeIndexes.index(ID)]
    rowA = [hylakID]
    rowWM = [hylakID]
    rowWS = [hylakID]
    rowLM = [hylakID]
    rowLS = [hylakID]
    rowWE = [hylakID]
    rowLE = [hylakID]
    Data = open(S1ResultsPath+f,'r')
    
    Lines = Data.readlines()
    Lines.pop(0)
    
    Area = []
    Dates = []
    Wmean = []
    Wstddev = []
    Lmean = []
    Lstddev = []
    WEr = []
    LEr = []

    for line in Lines:
        line = line.split('\t')
        date = int(line[0])
        area = float(line[1])
        wmean = float(line[2])
        wstd = float(line[3])
        lmean = float(line[4])
        lstd = float(line[5])
        werror = float(line[8])
        lerror = float(line[9][:-1])
        Dates.append(date)
        Area.append(area)
        Wmean.append(wmean)
        Wstddev.append(wstd)
        Lmean.append(lmean)
        Lstddev.append(lstd)
        WEr.append(werror)
        LEr.append(lerror)
        
        
    for d in hardcodeDates:
        d = int(datetime.datetime.timestamp(d - timedelta(days=1))*1000)
        if d in Dates:
            I = Dates.index(d)
            rowA.append(Area[I])
            rowWM .append(Wmean[I])
            rowWS.append(Wstddev[I])
            rowLM.append(Lmean[I])
            rowLS.append(Lstddev[I])
            rowWE.append(WEr[I])
            rowLE.append(LEr[I])
        else:
            rowA.append(-9999)
            rowWM .append(-9999)
            rowWS.append(-9999)
            rowLM.append(-9999)
            rowLS.append(-9999)
            rowWE.append(-9999)
            rowLE.append(-9999)
    
    Awriter.writerow(rowA)
    WMwriter.writerow(rowWM)
    WSwriter.writerow(rowWS)
    LMwriter.writerow(rowLM)
    LSwriter.writerow(rowLS)
    WEwriter.writerow(rowWE)
    LEwriter.writerow(rowLE)

AreaCSV.close()
WmeanCSV.close()
WStddevCSV.close()
LmeanCSV.close()
LStddevCSV.close()
WerrorCSV.close()
LerrorCSV.close()
    
    
    
    
    
    
