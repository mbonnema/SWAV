#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:35:01 2021

@author: mbonnema
"""

import numpy as np
def FilterS1(D,A,WE,LE):
    D_f = {}
    A_f = {}
    WE_f = {}
    LE_f = {}
    for key in D:
        dates = D[key]
        areas = A[key]
        werrors = WE[key]
        lerrors = LE[key]
        
        
        d_f = []
        a_f = []
        we_f = []
        le_f = []
        
        for d,a,we,le in zip(dates,areas,werrors,lerrors):
            #print(a)
            if we < 0:
                we = 0
            if le < 0:
                le = 0
            if a > 0:
                if we/a > 0.1:
                    #print('fail 1')
                    continue
            if a > 0:
                if le/a > 0.1:
                    #print('fail 2')
                    continue
            #print('passed')
            d_f.append(d)
            a_f.append(a)
            we_f.append(we)
            le_f.append(le)
        a_std = np.std(np.array(a_f))
        a_mean = np.mean(np.array(a_f))
        d_f = np.array(d_f)[np.array([a_f<=(a_mean+a_std*3),a_f>=(a_mean-a_std*3)]).all(axis=0)]
        we_f = np.array(we_f)[np.array([a_f<=(a_mean+a_std*3),a_f>=(a_mean-a_std*3)]).all(axis=0)]
        le_f = np.array(le_f)[np.array([a_f<=(a_mean+a_std*3),a_f>=(a_mean-a_std*3)]).all(axis=0)]
        a_f = np.array(a_f)[np.array([a_f<=(a_mean+a_std*3),a_f>=(a_mean-a_std*3)]).all(axis=0)]
        D_f[key] = d_f
        A_f[key] = a_f
        WE_f[key] = we_f
        LE_f[key] = le_f
        
    return(D_f,A_f,WE_f,LE_f)
            
        