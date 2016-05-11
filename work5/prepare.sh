#!/bin/bash

mkdir /tmp/mir
cd /tmp/mir

#cp /home/octavio/Dropbox/MIR/Datasets/*arff /tmp/mir
path_dropbox="/Users/octavio/Dropbox"
#path_dropbox="/Users/octavio/Dropbox"

tar zxvf $path_dropbox/MIR/Datasets/clasica.tgz
tar zxvf $path_dropbox/MIR/Datasets/jazz.tgz
tar zxvf $path_dropbox/MIR/Datasets/kar.tgz

#tar zxvf $path_dropbox/MIR/Datasets/clasica.tgz
#tar zxvf $path_dropbox/MIR/Datasets/jazz.tgz
#tar zxvf $path_dropbox/MIR/Datasets/kar.tgz

#cp $path_dropbox/MIR/cosas/work2/clasica.csv .
#cp $path_dropbox/MIR/cosas/work2/jazz.csv .
#cp $path_dropbox/MIR/cosas/work2/kar.csv .
