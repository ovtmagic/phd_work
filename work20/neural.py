#!/anaconda/bin/python

import os
from keras.models import Sequential
from keras.layers import Dense
import numpy

# convert arff to csv
def arff2csv(arff_filename):
    # num of attributes for arff file
    num_attr = 0
    
    # create tmp Folder
    if not os.path.exists("tmp"):
        print("Create tmp folder")
        os.mkdir("tmp")
    
    # read arff file
    header_readed = False
    csv = ""
    f = open(arff_filename)   
    for line in f.readlines():
        if header_readed:
            csv = csv + line
            # read num of attributes
            if num_attr == 0:
                num_attr = len(line.split(",")) - 1
        elif line.startswith("@data"):
            header_readed = True
    f.close()
    
    # format and write csv file
    csv = csv.replace("yes", "1")
    csv = csv.replace("no", "0")
    csv_filename = "tmp/" + arff_filename.split("/")[-1].replace(".arff", ".csv")
    f = open(csv_filename, 'w')     
    f.write(csv)
    f.close()        
    
    return csv_filename, num_attr
        
        
# class to implement neural network
#    layers: array with number of neurons in each layer, last layer must not be in this variable, it is always one
class TNeuralNet:
    
    def __init__(self, csv_train, csv_test, inputs, layers, seed=7):
        self.csv_train = csv_train
        self.csv_test = csv_test
        self.inputs = inputs
        self.layers = layers
        self.seed = seed
        
    def run(self):
        # fix random seed for reproducibility
        numpy.random.seed(self.seed)
        
        # load train and test databases
        dataset = numpy.loadtxt(self.csv_train, delimiter=",")
        # split into input (X) and output (Y) variables
        X = dataset[:,0:self.inputs]
        Y = dataset[:,self.inputs]
        
        dataset_test = numpy.loadtxt(self.csv_test, delimiter=",")
        # split into input (X) and output (Y) variables
        X_test = dataset_test[:,0:self.inputs]
        Y_test = dataset_test[:,self.inputs]
        
        
        # create model
        model = Sequential()
        # fist layer
        model.add(Dense(self.layers[0], input_dim=self.inputs, activation='relu'))
        # rest of layers
        for i in range(1,len(self.layers)):
            model.add(Dense(self.layers[i], activation='relu'))
        # last layer
        model.add(Dense(1, activation='sigmoid'))
        
        # Compile model
        print("- compile")
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        
        # Fit the model
        print("- fit")
        model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
        
        # evaluate the model
        print("- evaluates")
        scores = model.evaluate(X_test, Y_test)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))   
        result = scores[1]*100
        return result
        
        
        
        
if __name__ == "__main__":
    datasets_path = "../datasets/arff/"
    csv_train, num_attr = arff2csv(datasets_path + "m_kar_train.arff")
    csv_test, _ = arff2csv(datasets_path + "m_kar_test.arff")
    print("FILE: %s (attrs: %s)" % (csv_train, num_attr))
    print("FILE: %s (attrs: %s)" % (csv_test, num_attr))
    net = TNeuralNet(csv_train, csv_test, num_attr, [100, 80])
    result = net.run()
    print("Result: %s" % (result))
    
    