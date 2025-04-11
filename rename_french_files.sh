#!/bin/bash

# Script to rename files with French characters to English equivalents
# This script checks for existence before renaming

echo "Starting file renaming process..."

# Function to rename a file if it exists
rename_if_exists() {
    local source_file="$1"
    local target_file="$2"

    if [ -f "$source_file" ]; then
        echo "Renaming '$source_file' to '$target_file'"
        mv "$source_file" "$target_file"
        echo "✓ Done"
    else
        echo "× File not found: $source_file"
    fi
}

# 1. Rename files with French characters
echo -e "\n== Renaming files with French characters =="

# Handle the indexing system file
rename_if_exists "OOP-core/history/Système d'indexation dynamique des tags.py" "OOP-core/history/dynamic_tag_indexing_system.py"

# Handle the header structure file
rename_if_exists "OOP-core/history/structure de header.md" "OOP-core/history/header_structure.md"

# Handle the template system structure file
rename_if_exists "OOP-core/history/Structure du système de templates.md" "OOP-core/history/template_system_structure.md"

# 2. Look for other files with French accents that might need renaming
echo -e "\n== Checking for other files with potential French characters =="
find . -type f -name "*[éèêëàâäôöùûüçÉÈÊËÀÂÄÔÖÙÛÜÇ]*" | while read file; do
    echo "! Found file with accented characters: $file"
    echo "  Consider renaming this file manually."
done

echo -e "\nFile renaming complete."
echo "Please verify the changes before committing to Git."