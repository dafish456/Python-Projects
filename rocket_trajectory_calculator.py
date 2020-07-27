'goal: create a rocket trajectory calculator, meaning take'
'initial parameters and plot acceleration, thrust, remaining fuel?, altitude,'
'position'

#!/usr/bin/env python

import os    # standard library
import sys

#import requests  # 3rd party packages
'''import matplotlib.pylot as plt
import numpy as np'''

#import mypackage.mymodule  # local source
#import mypackage.myothermodule

__author__ = "Vishal Ravi"
__copyright__ = "Copyright 2020, DaFish Industries"
__credits__ = ["Vishal Ravi"]
__license__ = ""
__version__ = ""
__maintainer__ = "Vishal Ravi"
__email__ = "ravi43@purdue.edu"
__status__ = ""


#program flow: input parameters for rocket, generate array data for plots, pass data into matplot and plot data
'''get the flight time, set up intervals for x-axis (if uses time) and make a'''
class Rocket:
    
    def __init__(self, thrust):
        self.thrust = thrust #initial thrust in Newtons
        
        #calculate individual rocket flight time using init values
        self.ft = 4.056

    def time_axis(self, t_max):
        t = 0
        dt = 0.01
        time_arr = []
        while t <= t_max:
            time_arr.append(t)
            print(t)            
            t+=dt
    
    def position(yi, vi, ai): 
        return yi

    #def plot(y_axis, x_axis):
        
r1 = Rocket(5)
#time_axis(rocket_object.ft) #name 'time_axis' is not defined error
Rocket.time_axis(r1, r1.ft)
