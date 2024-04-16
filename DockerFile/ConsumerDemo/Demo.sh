#!/bin/bash

# Define the directories that contain the Python files
directories=("Audio" "Image" "Store" "Video")

# Iterate over the directories
for dir in "${directories[@]}"; do
    # Change to the directory
    cd "$dir"

    # Find all Python files and run them
    for file in *.py; do
        echo "Running $file in $dir"
        python3 "$file" &
    done

    # Change back to the parent directory
    cd -
done

# Wait for all background jobs to finish
wait