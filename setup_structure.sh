#!/bin/bash

# Define the base directory where the structure will be created
BASE_DIR="/path/to/your/base/directory"

# Define directories to be created
directories=(
    "$BASE_DIR/dir1"
    "$BASE_DIR/dir2/subdir1"
    "$BASE_DIR/dir3"
)

# Define files to be created with their content
declare -A files
files=(
    ["$BASE_DIR/dir1/file1.txt"]="Content for file1.txt"
    ["$BASE_DIR/dir2/subdir1/file2.txt"]="Content for file2.txt"
    ["$BASE_DIR/dir3/file3.txt"]="Content for file3.txt"
)

# Create directories if they don't exist
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "Created directory: $dir"
    else
        echo "Directory already exists: $dir"
    fi
done

# Create files with content if they don't exist
for file in "${!files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "${files[$file]}" > "$file"
        echo "Created file: $file"
    else
        echo "File already exists: $file"
    fi
done
