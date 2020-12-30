# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:02:17 2020

@author: bwhit
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
#import seaborn as sns
import random
import numpy as np

class World:
    def __init__(self, population, sizex, sizey):
        self.contact_distance = 5
        self.transmission_rate = 0.1
        self.recovery_period = 1
        self.incubation_period = 1
        self.reset_period = 1
        
        self.sizex = sizex
        self.sizey = sizey
        self.health = ("susceptible", "exposed", "infectious", "recovered")
        self.population = population
        self.people = list()
        self.init_population()
        self.init_distance()
        
    def init_population(self):
        for person in range(self.population):
            x = random.uniform(0, self.sizex)
            y = random.uniform(0, self.sizey)
            status = self.health[0]
            
            self.people.append([person, x, y, status, 0])
        
    def init_distance(self):
        self.distance_matrix = np.zeros([self.population, self.population])
        iteration = 0
        for index1 in range(self.population):
            #print("Iteration", iteration)
            person1 = self.people[index1]
            x1 = person1[1]
            y1 = person1[2]
            for index2 in range(self.population):
                person2 = self.people[index2]
                x2 = person2[1]
                y2 = person2[2]
                distance = np.sqrt((x1-x2)**2 + (y1-y2)**2)
                self.distance_matrix[index1, index2] = distance
            iteration = iteration+1
    
    def infect_random(self, number):
        for k in range(number):
            #infect one random person between [1, self.population]
            person = random.randint(0, self.population-1)
            self.people[person][3] = "infectious"
        self.initial_infection = number
        
    def update(self):
        self.people_update = self.people.copy()
        for index1 in range(self.population):
            num_days = self.people_update[index1][4]
            status = self.people_update[index1][3]
            if status == "exposed":
                num_days = num_days + 1
                if num_days >= self.incubation_period:
                    #print(num_days)
                    self.people_update[index1][3] = "infectious"
                    self.people_update[index1][4] = 0
                else:
                    self.people_update[index1][4] = num_days
            if status == "infectious":
                num_days = num_days + 1
                if num_days >= self.recovery_period:
                    self.people_update[index1][3] = "recovered"
                    self.people_update[index1][4] = 0
                else:
                    self.people_update[index1][4] = num_days
            if status == "recovered":
                num_days = num_days + 1
                if num_days >= self.reset_period:
                    self.people_update[index1][3] = "susceptible"
                    self.people_update[index1][4] = 0
                    
            if status == "infectious":
                for index2 in range(self.population):
                    if index1 != index2:
                        distance = self.distance_matrix[index1, index2]
                        status2 = self.people_update[index2][3]
                        if status2 == "susceptible":
                            if distance <= self.contact_distance:
                                number = random.uniform(0, 1)
                                if number <= self.transmission_rate:
                                    self.people_update[index2][3] = "exposed"
        self.people = self.people_update

#VARIABLES
num_people = 5000
sizex = 50
sizey = 50

world = World(num_people, sizex, sizey)

x = list()
y = list()

stats = list()

initial_infection = 2
world.infect_random(initial_infection)

for k in range(20):
    num_susceptible = 0
    num_exposed = 0
    num_infectious = 0
    num_recovered = 0
    for person in world.people:
        x.append(person[1])
        y.append(person[2])
        status = person[3]
        
        if status == "susceptible":
            color = "yellow"
            num_susceptible = num_susceptible + 1
        elif status == "exposed":
            color = "orange"
            num_exposed = num_exposed + 1
        elif status == "infectious":
            color = "purple"
            num_infectious = num_infectious + 1
        else:               #recovered
            color = (0.08, 0.706, 0.455)
            num_recovered = num_recovered + 1
            
        plt.plot(x[-1], y[-1], 'o', color = color)
    
    plt.grid(color='lightblue', alpha=0.5)
    plt.xlim([0,world.sizex])
    plt.ylim([0,world.sizey])
    
    plt.title(k+1)
        
    plt.show()
    
    world.update()
    stats.append([k, num_susceptible, num_exposed, num_infectious, num_recovered])
    #print("Susceptible, Exposed, Infectious, Recovered")
    #print(num_susceptible, num_exposed, num_infectious, num_recovered)

statsarray = np.array(stats)
plt.plot(statsarray[:,0], statsarray[:,1], label="Susceptible", color="gold")
plt.plot(statsarray[:,0], statsarray[:,2], label="Exposed", color="red")
plt.plot(statsarray[:,0], statsarray[:,3], label="Infectious", color="purple")
plt.plot(statsarray[:,0], statsarray[:,4], label="Recovered", color="green")
plt.legend()
plt.grid(color = "lightblue", alpha = 0.5)
plt.xlabel("Days")
plt.ylabel("Number of People")
plt.title("SIS Model")
plt.xlim([0,None])
plt.ylim([0,None])
plt.show()