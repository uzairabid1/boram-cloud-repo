#!/bin/bash

while true; do
    python naver.py  

    if [ -f "output_list10.csv.csv" ]; then
        tail -n 1 output_list10.csv.csv | sed -i '$ d' output_list10.csv.csv
        echo "Removed the last line from 'output_list10.csv.csv'"
    else
        echo "'output_list10.csv.csv' not found. Continuing without removing the last line."
    fi
    
    echo "Script stopped. Restarting in 10 seconds..."
    sleep 10
done
