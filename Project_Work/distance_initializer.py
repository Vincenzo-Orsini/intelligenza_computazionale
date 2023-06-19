import matplotlib.pyplot as plt
import numpy as np

from data_initializer import Shops_ground, Entrances, Entertainment_ground, Food_ground
from data_initializer import left_x, left_y, right_x, right_y, midleft_x, midleft_y, midright_x, midright_y, upper_x, upper_y, lower_x, lower_y

def distance_fixed(point):
    width = .1
    #print(point)
    for i in Shops_ground:
        if i[2] == point:
            x = i[6]
            #print(x)
            y = i[7]
            #print(y)
            initial_distance=i[8]
    for i in Food_ground:
        if i[2] == point:
            x = i[6]
            #print(x)
            y = i[7]
            #print(y)
            initial_distance=i[8]
    for i in Entertainment_ground:
        if i[2] == point:
            x = i[6]
            #print(x)
            y = i[7]
            #print(y)
            initial_distance=i[8]
    for i in Entrances:
        if i[2] == point:
            x = i[6]
            #print(x)
            y = i[7]
            #print(y)
            initial_distance=i[8]
    for j in range(len(midright_x)):
        if x == midright_x[j] and y == midright_y[j]:
            #print("midright")
            index = np.where(midright_x==x)[0][0]
            dist = initial_distance + (abs(midright_x[index]-midright_x[85]))*width
            return dist
    for j in range(len(lower_x)):
        if x == lower_x[j] and y == lower_y[j]:
            #print("lower")
            index = np.where(lower_x==x)[0][0]
            dist1 = initial_distance+(abs(lower_x[460]-lower_x[index]))*width
            #print(dist1)
            dist2 = abs(midright_x[0]-midright_x[85])*width
            #print(dist2)
            dist = dist1+dist2
            return dist
    for j in range(len(left_x)):
        if x == left_x[j] and y == left_y[j]:
            #print("left")
            index = np.where(left_y==y)[0][0]
            dist1 = initial_distance+(abs(left_y[index]-left_y[400]))*width
            dist2 = abs((lower_x[0])-lower_x[460])*width
            dist3 = abs(midright_x[0]-midright_x[85])*width
            dist = dist1+dist2+dist3
            return dist
    for j in range(len(midleft_x)):
        if x == midleft_x[j] and y == midleft_y[j]:
            #print("midleft")
            index = np.where(midleft_y==y)[0][0]
            if index<160:
                dist1 = initial_distance+abs(midleft_y[index]-midleft_y[0])*width
                #print(dist1)
                dist2 = abs(lower_x[215]-lower_x[460])*width
                #print(dist2)
                dist3 = abs(midright_x[0]-midright_x[85])*width
                #print(dist3)
                dist = dist1+dist2+dist3
                return dist
            else:
                dist1 = initial_distance+abs(midleft_y[index]-midleft_y[len(midleft_y)-1])*width
                dist2 = abs(upper_x[265]-upper_x[765])*width
                dist3 = abs(midright_x[len(midright_x)-1]-midright_x[85])*width
                dist = dist1+dist2+dist3
                return dist
    for j in range(len(upper_x)):
        if x == upper_x[j] and y == upper_y[j]:
            #print("upper")
            index = np.where(upper_x==x)[0][0]
            if index>130:
                dist1=initial_distance+abs(upper_x[index]-upper_x[765])*width
                dist2=abs(midright_x[len(midright_x)-1]-midright_x[85])*width
                dist = dist1+dist2
                return dist
            else:
                dist1=initial_distance+abs(upper_x[index]-upper_x[0])*width
                dist2=abs(left_x[len(left_x)-1]-left_x[400])*width
                dist3 = abs((lower_x[0])-lower_x[460])*width
                dist4 = abs(midright_x[0]-midright_x[85])*width
                dist = dist1+dist2+dist3+dist4
                return dist
    for j in range(len(right_x)):
        if x == right_x[j] and y == right_y[j]:
            #print("right")
            index = np.where(right_x==x)[0][0]
            if index<50:
                dist1 = initial_distance+abs(right_x[index]-right_x[0])*width
                dist2 = abs(lower_x[len(lower_x)-1]-lower_x[460])*width
                dist3 = abs(midright_x[len(midright_x)-1]-midright_x[85])*width
                dist = dist1+dist2+dist3
                return dist
            else:
                dist1 = initial_distance+abs(right_x[index]-right_x[len(right_x)-1])*width
                dist2 = abs(upper_x[len(upper_x)-1]-upper_x[765])*width
                dist3 = abs(midright_x[len(midright_x)-1]-midright_x[85])*width
                dist = dist1+dist2+dist3
                return dist

def distance(point1, point2):
    d = abs(distance_fixed(point1)-distance_fixed(point2))
    return d