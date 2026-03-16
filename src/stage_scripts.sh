#!/bin/bash

echo "Scanning for updated source code and documentation..."

# Safely add all Python files in the src directory
git add ~/physics-postdoc-pipeline/src/*.py

# Safely add all files in the doc directory
#git add doc/*

# Always ensure .gitignore is tracked
if [ -f .gitignore ]; then
    git add .gitignore
fi

echo -e "\n--- Files staged for commit ---"
# Show a clean, condensed status of what is about to be committed
git status
