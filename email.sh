# File to monitor
FILE_TO_MONITOR="/Users/songye03/Desktop/backtesting/signals.txt"

# Email settings
EMAIL="songyuye29@gmail.com"
BODY="The cron job has written to the file: $FILE_TO_MONITOR"

# # clear the file in case it has content
echo "" > "$FILE_TO_MONITOR"

# Monitor the file for changes using fswatch
{
timeout 60s fswatch -0 "$FILE_TO_MONITOR" | while read -d "" event; do
    # Send email when the file is modified
    echo -e "Subject: $SUBJECT\n\n$BODY" | msmtp "$EMAIL"
done
} &
