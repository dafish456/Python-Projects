#!/usr/bin/env python

import os    # standard library
import sys

#import requests  # 3rd party packages
'''import matplotlib.pylot as plt
import numpy as np'''

#import mypackage.mymodule  # local source
#import mypackage.myothermodule
import math

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
    
    def __init__(self, name, total_mass, prop_mass, max_thrust, time_maxThrust, burn_time):
        self.name = name
        self.total_mass = total_mass
        self.prop_mass = prop_mass
        self.max_thrust = max_thrust/1.0 #thrust in Newtons
        self.time_maxThrust = time_maxThrust
        self.burn_time = burn_time
        
        #calculate individual rocket flight time using init values
        self.ft = 5 #ft must be > burn_time duh
        
        #structural mass
        self.str_mass = self.total_mass - self.prop_mass

    def time_axis(self):
        t = 0
        dt = 0.01
        time_arr = []
        while t <= self.ft:
            time_arr.append(t)
            print(t)
            t+=dt
        return time_arr

    def get_mass(self, time):
        #advanced burn profile goes here: rate at which prop burns
        #estimated here
        if time == 0:
            current_total_mass = self.total_mass
        else:
            current_prop_mass = -1.0*(self.prop_mass/self.burn_time)*(time) + self.prop_mass
            if current_prop_mass <= 0:
                current_total_mass = self.str_mass
            else:
                current_total_mass = self.str_mass + current_prop_mass
        return current_total_mass

    def integrate(self, arrToIntegrate):
        integratedArr = []
        time_vals = self.time_axis()#####################
        #CONTINUE HERE BRUH -------------------------------------------
        i = 0
        while time_vals[i] < self.ft:
            pass
        return integratedArr
    
    def position(self, yi, vi, ai):
        #get 
        return yi

    def velocity(self, vi):
        #acc_values = self.acceleration()
        #use integrate function above to integrate acc to get vel
        pass
    
    def acceleration(self):
        acc_arr = []
        t = 0
        dt = 0.01
        while t <= self.ft:
            val = self.get_thrust(t)/self.get_mass(t)
            acc_arr.append(val)
            print('self.get_thrust(', t, ') / self.get_mass(t) = ', val)
            t+=dt
        return acc_arr
            
    def get_thrust(self, time):
        #insert better thrust profile here
        current_thrust = 0
        if time == 0:
            current_thrust = 0
        elif time < self.burn_time and time > 0:
            if time < self.time_maxThrust:
                current_thrust = self.max_thrust*math.exp(-(time - self.time_maxThrust)*(time - self.time_maxThrust))     
            elif time < 0.5:
                current_thrust = (-2*(time-self.time_maxThrust)*(time-self.time_maxThrust) + 1)*self.max_thrust
            elif time < self.burn_time:
                current_thrust = 0.392*self.max_thrust/time
        else:
            current_thrust = 0.1*self.max_thrust
        return current_thrust
        
    #def plot(y_axis, x_axis):

def main():
    r1 = Rocket('bruhRocket', 50, 10, 800, .17, 3.5)
    r1.acceleration()
    r1.velocity(0)
    print('------------------------------------------------------------------------------------------------------------------------------------------------------------')
    '''print('Enter your Rocket\'s name:')
    rocket_name = input()
    print('Enter ', rocket_name,'\'s total mass:')
    total_mass = input()
    print('Enter ', rocket_name,'\'s propellant mass:')
    prop_mass = input()
    print('Enter ', rocket_name,'\'s max thrust:')
    max_thrust = input()
    print('Enter ', rocket_name,'\'s burn duration:')
    burn_time = input()
    generate rocket object using inputs
    generate plots through Matplotlib using rocket object
    '''
    
    #time_axis(rocket_object.ft) #name 'time_axis' is not defined error
    #Rocket.time_axis(r1)

if __name__ == "__main__":
    main()
