#!/bin/bash

DIRECTORY="3-SAT"
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
    result=$(python3 main.py "$file" "$T_VALUE")
    echo $result

    # Extract the solving time and number of conflicts from the result
    solving_time=$(echo "$result" | grep "c total solving time:" | awk '{print $5}')
    splits=$(echo "$result" | grep "c number of splits:" | awk '{print $5}')

    # Add the solving time and number of splits to their respective totals
    TOTAL_TIME=$(echo "$TOTAL_TIME + $solving_time" | bc)
    TOTAL_SPLITS=$(echo "$TOTAL_CONFLICTS + $splits" | bc)
  fi
done

echo "Total solving time: $TOTAL_TIME"
echo "Total number of splits: $TOTAL_SPLITS"