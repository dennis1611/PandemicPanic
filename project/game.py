
import numpy as np
import Regions


#population = 17000000
#infected = population * 0.0001  # ideally save as list
R = 1.1
week = 0


#create regions
country = []

regions_data = np.genfromtxt("Regions_data.txt")


country.append(Regions.region("South-Holland",population))


running = True
while running:
    # def update infected ( += infected*R/2, -= people who recovered (maybe  - infected[i-3]  or something))

    # def display report in terminal

    # def choose 1 measure (with "none" as option too)

    # def update R based on chosen measure

    week += 1

    print(country[0].name,country[0].inhabitants)
    break

print("Normal end")