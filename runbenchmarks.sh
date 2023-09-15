#!/bin/bash

DIRECTORY="benchmarks"
TOTAL_TIME=0
TOTAL_CONFLICTS=0

# Get command line argument for 't' value
T_VALUE="$1"

# Check if directory exists
if [[ ! -d "$DIRECTORY" ]]; then
  echo "Directory $DIRECTORY does not exist."
  exit 1
fi

# Loop through all files in directory
for file in "$DIRECTORY"/*; do
  # Check if file is not a directory
  if [[ ! -d "$file" ]]; then

    # Run the python command with the file and 't' value as arguments, capture the output
    result=$(python main.py "$file" "$T_VALUE")

    # Extract the solving time and number of conflicts from the result
    solving_time=$(echo "$result" | grep "c total solving time:" | awk '{print $5}')
    conflicts=$(echo "$result" | grep "c number of conflicts:" | awk '{print $5}')

    # Add the solving time and number of conflicts to their respective totals
    TOTAL_TIME=$(echo "$TOTAL_TIME + $solving_time" | bc)
    TOTAL_CONFLICTS=$(echo "$TOTAL_CONFLICTS + $conflicts" | bc)
  fi
done

echo "Total solving time: $TOTAL_TIME"
echo "Total number of conflicts: $TOTAL_CONFLICTS"