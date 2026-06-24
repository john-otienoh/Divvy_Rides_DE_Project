#!/bin/bash
# combine_csvs.sh - Combine all CSV files in the downloads/ directory

set -euo pipefail

DOWNLOAD_DIR="downloads"
OUTPUT_FILE="downloads/combined.csv"

# Check if the directory exists
if [ ! -d "$DOWNLOAD_DIR" ]; then
    echo "Directory $DOWNLOAD_DIR does not exist."
    exit 1
fi

# Find CSV files, sorted alphabetically (optional)
CSV_FILES=($(ls "$DOWNLOAD_DIR"/*.csv 2>/dev/null | sort))

if [ ${#CSV_FILES[@]} -eq 0 ]; then
    echo "No CSV files found in $DOWNLOAD_DIR."
    exit 1
fi

# Write header from the first file
head -1 "${CSV_FILES[0]}" > "$OUTPUT_FILE"

# Append data from all files, skipping the header line in each
for file in "${CSV_FILES[@]}"; do
    tail -n +2 "$file" >> "$OUTPUT_FILE"
done

echo "Combined ${#CSV_FILES[@]} files into $OUTPUT_FILE"