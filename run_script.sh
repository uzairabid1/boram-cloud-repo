#!/bin/bash

while true; do
    python3 naver.py  

    if [ -f "output_list9.csv" ]; then
        tail -n 1 output_list9.csv | sed -i '$ d' output_list9.csv
        echo "Removed the last line from 'output_list9.csv'"
    else
        echo "'output_list9.csv' not found. Continuing without removing the last line."
    fi
    
    echo "Script stopped. Restarting in 10 seconds..."
    sleep 10
done
