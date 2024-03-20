#!/bin/bash

while true; do
    python naver.py  

    if [ -f "output_list4.csv" ]; then
        tail -n 1 output_list4.csv | sed -i '$ d' output_list4.csv
        echo "Removed the last line from 'output_list4.csv'"
    else
        echo "'output_list4.csv' not found. Continuing without removing the last line."
    fi
    
    echo "Script stopped. Restarting in 10 seconds..."
    sleep 10
done
