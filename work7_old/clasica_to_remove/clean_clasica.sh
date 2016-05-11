#!/bin/bash

list=(clasica/Berlioz_Hector_Absence.mid
clasica/Berlioz_Hector_AuCimeti.mid
clasica/Berlioz_Hector_LesNuits.mid
clasica/Berlioz_Hector_LeSpectre.mid
clasica/Berlioz_Hector_SurLes.mid
clasica/Berlioz_Hector_Villanelle.mid
clasica/brahms105_1.mid
clasica/burns_corn_rigs.mid
clasica/burns_last_may_braw_wooer.mid
clasica/mendel86_6.mid
clasica/mozmf14.mid)

for i in ${list[@]}
do
    echo $i
    mv $i clasica_to_remove
done
