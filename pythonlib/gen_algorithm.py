#!/anaconda/python/bin

import random
import copy

# Class example of items used in GeneticAlgoritm TGenAlg
# Following methods must be overwritten
# - initialize
# - evaluate (call to function to generate a result)
# - is_better
# - get_child
class TItemExample:
    def __init__(self):
        self.value = -1
        self.data = [-1, -1]
        self.dev = 1
    
    def initialize(self):
        for i in range(len(self.data)):
            x = random.random()
            x = int( x*100 )
            self.data[i] = x
        self.evaluate()
        
    def evaluate(self):
        v = 0
        for i in self.data:
            v = v + i
        self.value = v
    
    # compare two items
    def is_better(self, item):
        a = self.value
        b = item.value
        # nearest to value 4 (example)
        if abs(4-a) < abs(4-b):
            return True
        else:
            return False
    
   
    # create a child of the item       
    def get_child(self):
        new_item = copy.copy(self)
        new_item.value = self.value
        new_item.data = self.data.copy()
        for i in range(len(self.data)):
            delta = 1 + random.uniform(-1, 1) * self.dev
            new_item.data[i] = int(new_item.data[i] * delta) 
        new_item.evaluate()
        return new_item
    
    def print(self):
        print("%s: %s" %(self.value, self.data)) 

    
# Genetic algoritm
class TGA:
    def __init__(self, initial_pop):
        self.pop = initial_pop # initial population
        self.size_pop = len(initial_pop)

    # evaluate a generation (get values)
    def evaluate(self, pop):
        #print("len: %s" % len(pop))
        for p in pop:
            p.evaluate()
        return pop
    
    # return a population ordered, best first
    def order2(self):
        self.pop.sort(key=lambda k: k.value, reverse=False)
    
    def order(self):
        pop_ordered = []
        while self.pop:
            # search best
            best_i = 0
            for j in range(len(self.pop)):
                if self.pop[j].is_better(self.pop[best_i]):
                    best_i = j
            pop_ordered.append(self.pop[best_i])
            del self.pop[best_i]
        self.pop = pop_ordered           
                
            
        
    
    # get the next generation
    def get_next_generation(self, pop):
        next_pop = []
        for p in pop:
            next_pop.append(p.get_child())
        return next_pop
    
    def print(self, num=False):
        print("GENERATION: %s" % num)
        for i in self.pop:
            i.print()
            #print(i.data['value'])
        print("-------------------------------")
    
    # run genetic algorithm   
    def run(self, num_gen):
        # values for initial population
        self.pop = self.evaluate(self.pop)
        self.order()
        self.print(0)
        # generations
        for i in range(num_gen):
            next_gen = self.get_next_generation(self.pop)
            next_gen = self.evaluate(next_gen)
            self.pop = self.pop + next_gen
            self.order()
            self.pop = self.pop[0:self.size_pop]
            self.print(i+1)
            
            

            
if __name__ == "__main__":
    # initialize population
    pop = []
    for i in range(10):
        x = TItemExample()
        x.initialize()
        pop.append(x)
    ga = TGA(pop)
    ga.run(10)
