import individual
import random

POPULATION = 1000
NATURAL_RATE = 0.01

class Population:
    def __init__(self):
        self.population = []
        self.next_population = []
        self.generation = 1
        self.bestIndividial = 0
        for x in range(POPULATION):
            element = individual.Snake()
            self.population.append(element)

    def sort_by_fitness(self):
        self.population.sort(key = lambda pop: pop.fitness)
        self.bestIndividial = self.population[0]

    def natural_selection(self):
        survived = round(POPULATION * NATURAL_RATE, 0) # just to be safe
        for x in survived:
            survivor = self.population[x]
            self.next_population.append(survivor)


    def crossover(self, parent_1, parent_2):
        child = individual.Snake()
        [r, c] = parent_1.wih.shape
        rand_r = random.randint(0, r-1)
        rand_c = random.randint(0, c-1)
        # TODO finish cross over, and crossover
        # TODO need to check elements of lists and lengths because -1 elements -> done I think, but check again
        

    def new_generation(self):
        self.natural_selection()


        while len(self.next_population) < POPULATION:
            rand_1 = random.randint(0, POPULATION*NATURAL_RATE-1) 
            rand_2 = random.randint(0, POPULATION*NATURAL_RATE-1) 
            parent_1 = self.population[rand_1]
            parent_2 = self.population[rand_2]
            self.crossover(parent_1, parent_2)



this = Population()
print(this.population)
