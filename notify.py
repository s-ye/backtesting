import os
import smtplib
from email.message import EmailMessage

def check_file(file_path):
    """Check if the file at file_path is non-empty."""
    return os.path.getsize(file_path) > 0

def send_email(subject, body, to_email, from_email, password):
    """Send an email with the given subject and body."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    # Connect to the server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.send_message(msg)
        print("Email sent successfully")

def main():
    filepath = '/Users/songye03/Desktop/backtesting/signals.txt'
    to_email = 'songyuye29@gmail.com'
    from_email = 'songyuye29@gmail.com'
    password = 'qpkk fbdf mhtb gtoc'

    if check_file(filepath):
        subject = 'Trading signals updated'
        with open(filepath, 'r') as file:
            body = file.read()
        send_email(subject, body, to_email, from_email, password)
    else:
        print("No signals to send")

if __name__ == "__main__":
    main()