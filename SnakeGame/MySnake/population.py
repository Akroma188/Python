import individual
import random

POPULATION = 5

class Population:
    def __init__(self):
        self.population = []
        for x in range(POPULATION):
            element = individual.Snake()
            self.population.append(element)

this = Population()
print(this.population)
