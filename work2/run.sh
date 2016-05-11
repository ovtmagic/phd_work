#!/bin/bash

for i in `cat list.txt`
do
    echo File $i > txt
    smf2txt kar/$i|grep track >> txt
    cp kar/$i ${i}.mid
    rosegarden ${i}.mid
done