#!/usr/bin/python

import time


class Timing:
    def __init__(self):
        self.array={}
        
    def add(self,name):
        self.array[name]={}
        self.array[name]['total']=0.0
        
        
    def start(self,name):
        if(not name in self.array.keys() ):
            self.add(name)
        self.array[name]['start']=time.time()
        
    def stop(self,name):
        self.array[name]['stop']=time.time()
        self.array[name]['total'] = self.array[name]['total'] + ( self.array[name]['stop'] - self.array[name]['start'] )
        
    def get(self,name):
        return self.array[name]['total']
    
    def imp(self):
        for name in self.array.keys():
            print " * ",name,": ",self.get(name)
            
            
        
testTime=Timing()

            