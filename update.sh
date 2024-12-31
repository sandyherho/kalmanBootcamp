#!/bin/bash

# Function to display usage
function usage {
    echo "Usage: $0 [-m commit_message] [-b branch_name]"
    echo "  -m: Commit message (default: 'update')"
    echo "  -b: Branch to push to (default: 'main')"
    exit 1
}

# Default values
commit_message="update"
branch_name="main"

# Parse command-line options
while getopts "m:b:h" opt; do
    case $opt in
        m) commit_message="$OPTARG" ;;
        b) branch_name="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Check if the current directory is a git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Error: Not a git repository."
    exit 1
fi

# Add changes to the staging area
git add .
if [ $? -ne 0 ]; then
    echo "Error: Failed to stage changes."
    exit 1
fi

# Commit changes with the specified message
git commit -m "$commit_message"
if [ $? -ne 0 ]; then
    echo "Error: Commit failed."
    exit 1
fi

# Push changes to the specified branch
git push origin "$branch_name"
if [ $? -ne 0 ]; then
    echo "Error: Push to branch '$branch_name' failed."
    exit 1
fi

# Success message
echo "Changes successfully pushed to branch '$branch_name' with commit message: '$commit_message'"

