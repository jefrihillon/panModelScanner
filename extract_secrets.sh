#!/bin/bash
# Script to extract secrets from .env file to individual files

if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# Extract values from .env file
grep MODEL_SECURITY_CLIENT_ID .env | cut -d '=' -f2 > id.txt
grep MODEL_SECURITY_CLIENT_SECRET .env | cut -d '=' -f2 > secret.txt
grep TSG_ID .env | cut -d '=' -f2 > tsg.txt
chmod 600 id.txt secret.txt tsg.txt

echo "Secret files created:"
echo "- id.txt"
echo "- secret.txt"
echo "- tsg.txt"
echo ""
echo "Make sure to keep these files secure and never commit them to version control!"