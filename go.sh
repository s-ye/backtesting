#!/bin/bash

# Activate the virtual environment (if needed)
source /Users/songye03/Desktop/backtesting/.venv/bin/activate

# Clear the overview text files
find /Users/songye03/Desktop/backtesting/monitor/ -name 'overview_*.txt' -exec truncate -s 0 {} \;

# Signal file
SIGNAL_FILE="/Users/songye03/Desktop/backtesting/signals.txt"

# Clear the file in case it has content
echo "" > "$SIGNAL_FILE"
truncate -s 0 "$SIGNAL_FILE"

# Run your Python script that generates the output
python /Users/songye03/Desktop/backtesting/monitor.py

python /Users/songye03/Desktop/backtesting/notify.py

# Navigate to the second repository where you want to push the folder
cd /Users/songye03/Desktop/me/

# Copy the generated folder to the second repo (replace with the actual output folder path)
cp -r /Users/songye03/Desktop/backtesting/monitor /Users/songye03/Desktop/me/

# Stage the changes
git add .

# Commit the changes (automate a commit message with timestamp or custom message)
git commit -m "Auto-commit: Update output folder on $(date)"

# Push the changes to the remote repository
git push origin main
