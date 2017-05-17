#!/anaconda/bin/python

import neural
import imp
import copy
import random
gen_algorithm = imp.load_source('gen_algorithm', '../pythonlib/gen_algorithm.py')



# Class example of items used in GeneticAlgoritm 
class TItem:
    def __init__(self, num_attr, csv_train, csv_test):
        self.value = -1
        self.data = [-1, -1]
        self.dev = 0.5
        self.num_attr = num_attr
        self.csv_train = csv_train
        self.csv_test = csv_test
    
    def initialize(self):
        for i in range(len(self.data)):
            x = random.random()
            x = int( x*100 )
            self.data[i] = x
        #self.evaluate()
        
    def evaluate(self):
        net = neural.TNeuralNet(self.csv_train, self.csv_test, self.num_attr, self.data)
        self.value = net.run()
        #print("Result: %s" % (self.value))
    
    # compare two items
    def is_better(self, item):
        a = self.value
        b = item.value
        # nearest to value 4 (example)
        if a > b:
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
        #new_item.evaluate()
        return new_item
    
    def print(self):
        print("%s: %s" %(self.value, self.data)) 





# create csv database
datasets_path = "../samples/0/arff"
genres = ["kar", "jazz", "class"]
track_type = ["m", "b"]
pop_size = 15
num_generations = 20

for t in track_type:
    for g in genres:
        csv_train, num_attr = neural.arff2csv("%s/%s_%s_train.arff" % (datasets_path, t, g))
        csv_test, _ = neural.arff2csv("%s/%s_%s_test.arff" % (datasets_path, t, g))
        print("FILE: %s (attrs: %s)" % (csv_train, num_attr))
        print("FILE: %s (attrs: %s)" % (csv_test, num_attr))
        
        # Genetic algoritm
        # initialize population
        pop = []
        for i in range(pop_size):
            x = TItem(num_attr, csv_train, csv_test)
            x.initialize()
            pop.append(x)
        ga = gen_algorithm.TGA(pop)
        results = ga.run(num_generations)
        
        # save results
        out_file = "tmp/result_%s_%s.txt" % (t,g)
        f = open(out_file, "w")
        for i in results:
            f.write("%s: %s\n" % (i.value, i.data))
        f.close()
