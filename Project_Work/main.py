import matplotlib.pyplot as plt
import numpy as np
import random
from deap import base, creator, tools

from data_initializer import Shops_ground, Entrances, Entertainment_ground, Food_ground
from data_initializer import left_x, left_y, right_x, right_y, midleft_x, midleft_y, midright_x, midright_y, upper_x, upper_y, lower_x, lower_y
from distance_initializer import distance, distance_fixed

IND_SIZE=int(input("How many shops are you going to visit (except where you already are): "))


SHOP_LIST = [Shops_ground[i][2] for i in range(len(Shops_ground))]
FOOD_LIST = [Food_ground[i][2] for i in range(len(Food_ground))]
ENT_LIST = [Entertainment_ground[i][2] for i in range(len(Entertainment_ground))]

ALL_LIST = []

for i in range(len(Shops_ground)):
    ALL_LIST.append(Shops_ground[i][2])
for i in range(len(Food_ground)):
    ALL_LIST.append(Food_ground[i][2])
for i in range(len(Entertainment_ground)):
    ALL_LIST.append(Entertainment_ground[i][2])

print("Shops Available")
print(SHOP_LIST)

print("Food-Shop Available")
print(FOOD_LIST)

print("Entertainment")
print(ENT_LIST)

#print(ALL_LIST)
#user_list=[]
tick = 0
starting_point = input("In which shop are you now? (Leave Blank if not, we'll consider the entrance): ")

while starting_point not in ALL_LIST and starting_point != "":
    print("You wrote a shop that is not in our mall or isn't spelled correctly. Please retry")
    shop = input("Write a Shop: ")
            
if starting_point=="":
    starting_point="Entrance 1"
    
user_list = []
for i in range(IND_SIZE):
    shop = input("Write a Shop: ")
    while shop not in ALL_LIST:
        print("You wrote a shop that is not in our mall or isn't spelled correctly. Please retry")
        shop = input("Write a Shop: ")
    while shop in user_list:
        print("You Wrote the same Shop more than once. Retry ")
        shop = input("Write a Shop: ")
    user_list.append(shop)
IND_SIZE+=1
    
print("Your selection is: ", user_list)
user_list.append(starting_point)
    
    
ending_point = input("From the selected ones, choose a place you want to visit last? (Leave blank if not, we'll consider the exit)")
while ending_point != "" and ending_point not in user_list:
    print("You picked a shop that is not in the selected list, retry ")
    ending_point = input("From the selected ones, choose a place you want to visit last? (Leave blank if not, we'll consider the exit)")
if ending_point=="":
    ending_point = "Entrance 2"
    user_list.append(ending_point)
    IND_SIZE+=1
    
print("Done")


np.random.seed(0)

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

TOURN_SIZE = 3 #Size of tournament block

#Initialization of our random selector
toolbox = base.Toolbox()
toolbox.register('attr_string', lambda: random.sample(user_list, IND_SIZE))

#Operators
#Crossover
toolbox.register('mate', tools.cxTwoPoint)
#Mutation
toolbox.register('mutate', tools.mutShuffleIndexes, indpb=0.05)
#Selection
toolbox.register('select', tools.selTournament, tournsize=TOURN_SIZE)


def evaluate(individual, starting_point=starting_point, ending_point=ending_point):
    fit = 0
    for i in range(len(individual)):
        counter = 0
        if individual[0] != starting_point:
            return 100
        elif individual[len(individual)-1]!=ending_point:
            return 100
        for j in range(len(individual)):
            if individual[i]==individual[j]:
                if individual[i]!="Entrance 1" or individual[i]!="Entrance 2":
                    counter +=1
                else:
                    counter +=0
        if counter >=2:
            return 100
    for i in range(len(individual)-1):
        fit += distance(individual[i], individual[i+1])
    return fit

toolbox.register('evaluate', evaluate)

#Statistical Features
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

def GA(POP_SIZE, CXPB, MUTPB, NGEN, stats, starting_point, ending_point, size=IND_SIZE): #other than the usual arguments, the function takes also the weights and values specified and the size of our problem
    #Defininf Hall of Fame
    hof = tools.HallOfFame(1)
    #HOF = [] #List created in order to store the best-weight (the maximum under the treshold) processed for every generation
    
    #Creating the population
    #individuals
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.attr_string) #here we can decide which size of our problem we are considering
    #population
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    
    pop = toolbox.population(n=POP_SIZE)
    #print(pop)

    #Defining the Logbook
    logbook = tools.Logbook()
    logbook.header = ["gen", "nevals"] + (stats.fields if stats else[])

    #Evaluate the entire population
    fitness = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitness):
        ind.fitness.values = [fit]
        #print(fit)


    hof.update(pop) if stats else {}

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals=len(pop), **record)
    

    for g in range(NGEN):
        #Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        #Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        #Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2],offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1,child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        #Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitness = list(map(toolbox.                                                                                                                   evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitness):
            ind.fitness.values = [fit]
            #print(fit)
        if hof is not None:
            hof.update(offspring)

        #The population in entirely replaced by the offspring
        pop[:] = tools.selBest(offspring, POP_SIZE-1)
        pop.append(hof[0])
        #HOF.append(hof[0]) #here, for instance, we add the best individual for eache iteration (generation) to the HOF list created above


        record = stats.compile(pop) if stats else{}
        logbook.record(gen=g+1, nevals=len(invalid_ind), **record)
        
        
    fitness_best = list(map(toolbox.evaluate, pop))
    for fit in fitness_best:
        if fit == min(fitness_best):
            index = fitness_best.index(fit)
    best = pop[index]
        
    return pop, logbook, best


if len(user_list)<5:
    NGEN = 70
elif 5<=len(user_list)<7:
    NGEN = 100
else:
    NGEN = 200
    


GA_exe = GA(POP_SIZE=40,CXPB=0.9,MUTPB=0.2,NGEN=NGEN, stats=stats, starting_point=starting_point, ending_point=ending_point)

print(GA_exe[1])
print(GA_exe[2])


min_values = [GA_exe[1][i]['min'] for i in range(len(GA_exe[1]))]
ngen = [i for i in range(len(GA_exe[1]))]

plt.figure(figsize=(16,12))
plt.ylabel("NGen")
plt.xlabel("Min Value")
plt.plot(ngen, min_values)
plt.grid()
plt.show()

