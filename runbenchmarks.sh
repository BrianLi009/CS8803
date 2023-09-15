#!/bin/bash

DIRECTORY="benchmarks"
TOTAL_TIME=0

# Check if directory exists
if [[ ! -d "$DIRECTORY" ]]; then
  echo "Directory $DIRECTORY does not exist."
  exit 1
fi

# Loop through all files in the directory
for file in "$DIRECTORY"/*; do
  # Check if file is not a directory
  if [[ ! -d "$file" ]]; then
    # Start timer
    start=$(date +%s.%N)

    # Run the python command with the file as argument
    python main.py "$file" t

    # Stop timer and calculate elapsed time
    end=$(date +%s.%N)
    elapsed=$(echo "$end - $start" | bc)
    TOTAL_TIME=$(echo "$TOTAL_TIME + $elapsed" | bc)
  fi
done

echo "Total time spent: $TOTAL_TIME seconds"