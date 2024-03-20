#!/bin/bash

while true; do
    python naver.py  

    if [ -f "output_list5.csv" ]; then
        tail -n 1 output_list5.csv | sed -i '$ d' output_list5.csv
        echo "Removed the last line from 'output_list5.csv'"
    else
        echo "'output_list5.csv' not found. Continuing without removing the last line."
    fi
    
    echo "Script stopped. Restarting in 10 seconds..."
    sleep 10
done
