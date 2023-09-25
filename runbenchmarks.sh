#!/bin/bash

declare -a solving_times
declare -a splits
TOTAL_TIME=0
TOTAL_SPLITS=0
SATISFIABLE_COUNT=0

# Get command line argument for 't' value
T_VALUE="$1"
DIRECTORY="$2"

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

    # If result contains "s SATISFIABLE", increment the counter
    if [[ $result == *"s SATISFIABLE"* ]]; then
      ((SATISFIABLE_COUNT++))
    fi

    # Extract the solving time and number of conflicts from the result
    solving_time=$(echo "$result" | grep "c total solving time:" | awk '{print $5}')
    splits=$(echo "$result" | grep "c number of splits:" | awk '{print $5}')

    # Store the solving time and number of splits
    solving_times+=($solving_time)
    splits+=($splits)

    # Add the solving time and number of splits to their respective totals
    TOTAL_TIME=$(echo "$TOTAL_TIME + $solving_time" | bc)
    TOTAL_SPLITS=$(echo "$TOTAL_SPLITS + $splits" | bc)
  fi
done

# Sort and find the median for solving times and splits
IFS=$'\n' sorted_solving_times=($(sort -n <<<"${solving_times[*]}"))
IFS=$'\n' sorted_splits=($(sort -n <<<"${splits[*]}"))

middle_index=$((${#sorted_solving_times[@]}/2))
if (( ${#sorted_solving_times[@]}%2 == 0 )); then
  median_solving_time=$(echo "scale=2; (${sorted_solving_times[$middle_index]} + ${sorted_solving_times[$middle_index-1]}) / 2" | bc)
  median_splits=$(echo "scale=2; (${sorted_splits[$middle_index]} + ${sorted_splits[$middle_index-1]}) / 2" | bc)
else
  median_solving_time=${sorted_solving_times[$middle_index]}
  median_splits=${sorted_splits[$middle_index]}
fi

echo "Total solving time: $TOTAL_TIME"
echo "Median solving time: $median_solving_time"
echo "Total number of splits: $TOTAL_SPLITS"
echo "Median number of splits: $median_splits"

echo "Number of satisfiable: $SATISFIABLE_COUNT"