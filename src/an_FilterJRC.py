#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:35:01 2021

@author: mbonnema
"""

def FilterJRC(D,A,N):
    D_f = {}
    A_f = {}
    N_f = {}
    for key in D:
        dates = D[key]
        areas = A[key]
        nodata = N[key]
        
        
        d_f = []
        a_f = []
        n_f = []
        
        for d,a,n in zip(dates,areas,nodata):
            #print(a)
            if n > 0.01:
                continue
            d_f.append(d)
            a_f.append(a)
            n_f.append(n)
        D_f[key] = d_f
        A_f[key] = a_f
        N_f[key] = n_f
        
    return(D_f,A_f,N_f)
            
        