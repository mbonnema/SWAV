#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:44:13 2020

@author: mbonnema
"""

from Sentinel1LakeArea_Ver2 import GetS1ResTimeSeries

import ee
ee.Initialize()

def RunS1TimeSeries(roi):
    startYear = 2017
    endYear = 2019
    R = [[],[],[],[],[],[],[],[],[],[]]
    
    while startYear <= endYear:
        startString = str(startYear)+'-01-01'
        endString = str(startYear)+'-12-31'
        print('\tBegin Processing Year '+str(startYear))
        startYear = startYear+1
        results = GetS1ResTimeSeries(roi,startString,endString)
        E = []
        try:
            Date = results[1].getInfo()
            print('\t\tRetrieved Dates')
            Water = results[0].getInfo()
            print('\t\tRetrieved Water Area')
            WPixM = results[2].getInfo()
            WPixS = results[3].getInfo()
            print('\t\tRetrieved WPix Stats')
            LPixM = results[4].getInfo()
            LPixS = results[5].getInfo()
            print('\t\tRetrieved LPix Stats')
            wProbThresh = results[6].getInfo()
            print('\t\tRetrieved wProbThresh')
            wThresh = results[7].getInfo()
            wError = results[8].getInfo()
            lError = results[9].getInfo()
            print('\t\tRetrieved Classification Errors')
        except Exception as e:
            Date = startString
            Water = -9999
            WPixM = -9999
            WPixS = -9999
            LPixM = -9999
            LPixS = -9999
            wProbThresh = -9999
            wThresh = -9999
            wError = -9999
            lError = -9999
            errorString = str(e)
            E.append(errorString)
        newResults = [Water,Date,WPixM,WPixS,LPixM,LPixS,wProbThresh,wThresh, wError, lError]
        NewR = []
        for old, new in zip(R, newResults):
            old.extend(new)
            NewR.append(old)
        R = NewR
        print('\tCompleted '+str(startYear-1))
    return R, E
            

