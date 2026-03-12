#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install Homebrew first:"
    echo "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Check if cwebp is installed
if ! command -v cwebp &> /dev/null; then
    echo "cwebp (WebP converter) is not installed."
    echo "Please install it using Homebrew: brew install webp"
    exit 1
fi

# Create the webp directory if it doesn't exist
mkdir -p webp

echo "Starting PNG to WebP conversion and resizing..."

# Iterate through all PNG files in the png directory
for file in png/*.png; do
  # Get the filename without the extension
  filename=$(basename "$file" .png)
  output_path="webp/$filename.webp"

  # Convert and resize the image
  # -resize 1000 0 means resize to 1000px width, 0 for height maintains aspect ratio
  cwebp "$file" -o "$output_path" -resize 1000 0

  if [ $? -eq 0 ]; then
    echo "Converted: $file -> $output_path"
  else
    echo "Failed to convert: $file"
  fi
done

echo "Conversion complete."
