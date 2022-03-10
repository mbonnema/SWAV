#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 13:22:48 2021

@author: mbonnema
"""
import datetime
from datetime import timedelta
import numpy as np

def InterpJRC(D,A):
    hardcodeDates = [datetime.datetime(2017, 1, 1, 16, 0), datetime.datetime(2017, 2, 1, 16, 0), datetime.datetime(2017, 3, 1, 16, 0), datetime.datetime(2017, 4, 1, 17, 0), datetime.datetime(2017, 5, 1, 17, 0), datetime.datetime(2017, 6, 1, 17, 0), datetime.datetime(2017, 7, 1, 17, 0), datetime.datetime(2017, 8, 1, 17, 0), datetime.datetime(2017, 9, 1, 17, 0), datetime.datetime(2017, 10, 1, 17, 0), datetime.datetime(2017, 11, 1, 17, 0), datetime.datetime(2017, 12, 1, 16, 0), datetime.datetime(2018, 1, 1, 16, 0), datetime.datetime(2018, 2, 1, 16, 0), datetime.datetime(2018, 3, 1, 16, 0), datetime.datetime(2018, 4, 1, 17, 0), datetime.datetime(2018, 5, 1, 17, 0), datetime.datetime(2018, 6, 1, 17, 0), datetime.datetime(2018, 7, 1, 17, 0), datetime.datetime(2018, 8, 1, 17, 0), datetime.datetime(2018, 9, 1, 17, 0), datetime.datetime(2018, 10, 1, 17, 0), datetime.datetime(2018, 11, 1, 17, 0), datetime.datetime(2018, 12, 1, 16, 0), datetime.datetime(2019, 1, 1, 16, 0), datetime.datetime(2019, 2, 1, 16, 0), datetime.datetime(2019, 3, 1, 16, 0), datetime.datetime(2019, 4, 1, 17, 0), datetime.datetime(2019, 5, 1, 17, 0), datetime.datetime(2019, 6, 1, 17, 0), datetime.datetime(2019, 7, 1, 17, 0), datetime.datetime(2019, 8, 1, 17, 0), datetime.datetime(2019, 9, 1, 17, 0), datetime.datetime(2019, 10, 1, 17, 0), datetime.datetime(2019, 11, 1, 17, 0), datetime.datetime(2019, 12, 1, 16, 0), datetime.datetime(2020, 1, 1, 16, 0)]
    masterDates = []
    for d in hardcodeDates:
        #d = int(datetime.datetime.timestamp(d - timedelta(days=1))*1000)
        d = int(datetime.datetime.timestamp(d)*1000)
        masterDates.append(d)
    
    D_f = {}
    A_f = {}
    
    for key in D:
        try:
            #print(str(key)+' started')
            dates = np.array(D[key])
            areas = np.array(A[key])
            
            d_f = []
            a_f = []
            
            for d in masterDates:
                if d in dates:
                    #print('\tNo interp for '+str(d))
                    I = dates == d
                    d_f.append(d)
                    a_f.append(areas[I])
                else:
                    ddiff = dates-d
                    if len(ddiff[ddiff<0]) == 0:
                        #print('\tFront interp for '+str(d))
                        d_f.append(d)
                        a_f.append(areas[0])

                    elif len(ddiff[ddiff>0]) == 0:
                        #print('\tBack interp for '+str(d))
                        d_f.append(d)
                        a_f.append(areas[-1])

                    else:
                        #print('\tMiddle interp for '+str(d))
                        d1 = dates[ddiff<0][-1]
                        d2 = dates[ddiff>0][0]
                        a1 = areas[ddiff<0][-1]
                        a2 = areas[ddiff>0][0]
                        
                        a = a1 + (d-d1)*(a2-a1)/(d2-d1)
                        a_f.append(a)

            a_f2 = []
            for a in a_f:
                a = float(a)
                a_f2.append(a)
            D_f[key] = np.array(d_f)
            A_f[key] = np.array(a_f2)

            #print(str(key)+' sucess')
        except Exception as e:
            #print(str(key)+' failed')
            
            print('error interpolating lake #'+str(key)+' Error: ' + str(e))
            continue
    return(D_f,A_f)
                