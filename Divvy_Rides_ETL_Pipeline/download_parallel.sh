#!/bin/bash
# download_parallel.sh – Concurrently download Divvy tripdata ZIPs with curl

DOWNLOAD_DIR="data/raw"
mkdir -p "$DOWNLOAD_DIR"

# List of URLs (same as your Python script)
URLS=(
    "https://divvy-tripdata.s3.amazonaws.com/202605-divvy-tripdata.zip"
    "https://divvy-tripdata.s3.amazonaws.com/202604-divvy-tripdata.zip"
    "https://divvy-tripdata.s3.amazonaws.com/202603-divvy-tripdata.zip"
    "https://divvy-tripdata.s3.amazonaws.com/202602-divvy-tripdata.zip"
    "https://divvy-tripdata.s3.amazonaws.com/202601-divvy-tripdata.zip"
)

# Export the download directory so the subshell can see it
export DOWNLOAD_DIR

# Define a function that downloads a single file
download_file() {
  local url="$1"
  local filename="${url##*/}"               # extract filename from URL
  echo "Starting: $filename"
  curl -sS --retry 3 --retry-delay 2 -L -o "$DOWNLOAD_DIR/$filename" "$url"
  if [ $? -eq 0 ]; then
    echo "Done: $filename"
  else
    echo "FAILED: $filename" >&2
  fi
}

# Make the function available to subshells
export -f download_file

# Print all URLs and pipe to xargs to run up to 4 downloads concurrently
printf "%s\n" "${URLS[@]}" | xargs -P 5 -I {} bash -c 'download_file "{}"'