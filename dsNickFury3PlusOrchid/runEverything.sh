#!/bin/bash

CHR=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "M" "X" "Y")
for i in "${CHR[@]}"
do
    :
    python chromosomeRunner.py --chromosome $i
done
