#!/usr/bin/env python

import os    # standard library
import sys

#import requests  # 3rd party packages
import matplotlib.pyplot as plt

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
    
    def __init__(self, name, total_mass, prop_mass, max_thrust, time_maxThrust, burn_time, height):
        self.name = name
        self.total_mass = total_mass
        self.prop_mass = prop_mass
        self.max_thrust = max_thrust/1.0 #thrust in Newtons
        self.time_maxThrust = time_maxThrust
        self.burn_time = burn_time
        self.height = height
        #calculate individual rocket flight time using init values

        self.ft = burn_time*5 #ft must be > burn_time duh
        
        #structural mass
        self.str_mass = self.total_mass - self.prop_mass

    def time_axis(self):
        t = 0
        dt = 0.01
        time_arr = []
        while t <= self.ft:
            time_arr.append(t)
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

    def integrate(self, arrToIntegrate, respectTo, initVal):
        integratedArr = []
        if respectTo == 'time':
            t = 0
            arr_pos = 0
            dt = 0.01
            while t < self.ft:
                if t !=0:
                    integratedArr.append(integratedArr[arr_pos - 1] + (arrToIntegrate[arr_pos]+arrToIntegrate[arr_pos - 1])*dt/2)
                else:
                    integratedArr.append(initVal)
                #print('@ t=', t, ', F(x) = ', integratedArr[arr_pos])
                arr_pos+=1
                t+=dt
        return integratedArr
    
    def position(self):
        return self.integrate(self.velocity(), 'time', self.height)

    def velocity(self):
        return self.integrate(self.acceleration(), 'time', 0)
            
    def acceleration(self):
        acc_arr = []
        t = 0
        dt = 0.01
        while t <= self.ft:
            val = (self.get_thrust(t) - 9.81*self.get_mass(t))/self.get_mass(t)
            acc_arr.append(val)
            #print('@t = ,', t, ', a = ', val)
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
            current_thrust = 0
        return current_thrust

    def shorten_arr(self, arr, indexCutoff):
        del arr[indexCutoff:]
        return arr
        
    def plot(y_axis, x_axis):
        pass
def main():
    print('Enter your Rocket\'s name:')
    rocket_name = input()
    print('Enter ', rocket_name,'\'s total mass:')
    total_mass = float(input())
    print('Enter ', rocket_name,'\'s propellant mass:')
    prop_mass = float(input())
    print('Enter ', rocket_name,'\'s max thrust:')
    max_thrust = float(input())
    print('Enter ', rocket_name,'\'s time at max thrust:')
    t_maxThrust = float(input())
    print('Enter ', rocket_name,'\'s burn duration:')
    burn_time = float(input())
    print('Enter ', rocket_name,'\'s height:')
    h = float(input())
    r1 = Rocket(rocket_name, total_mass, prop_mass, max_thrust, t_maxThrust, burn_time, h)
    
    t = 0
    dt = .01
    acc = r1.acceleration()
    vel = r1.velocity()
    pos = r1.position()
    a=0
    while pos[a] > 0:
        a+=1
        t+=dt
    r1.ft = t
    new_acc = r1.shorten_arr(acc, a+1)
    new_vel = r1.shorten_arr(vel, a+1)
    new_pos = r1.shorten_arr(pos, a+1)

    plt.figure(0)
    plt.ylabel('Altitude')
    plt.xlabel('Time')
    plt.plot(r1.time_axis(), new_pos)

    plt.figure(1)
    plt.ylabel('Velocity')
    plt.xlabel('Time')
    plt.plot(r1.time_axis(), new_vel)

    plt.figure(2)
    plt.ylabel('Acceleration')
    plt.xlabel('Time')
    plt.plot(r1.time_axis(), new_acc)
    plt.show()
if __name__ == "__main__":
    main()
    
