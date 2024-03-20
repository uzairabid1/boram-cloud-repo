#!/bin/bash

while true; do
    python3 naver.py  

    if [ -f "output_list1.csv" ]; then
        tail -n 1 output_list1.csv | sed -i '$ d' output_list1.csv
        echo "Removed the last line from 'output_list1.csv'"
    else
        echo "'output_list1.csv' not found. Continuing without removing the last line."
    fi
    
    echo "Script stopped. Restarting in 10 seconds..."
    sleep 10
done
