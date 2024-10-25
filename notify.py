# check whether a local .txt file is nonempty
# if it is, then we will send an email to ourselves

import os
import smtplib
from email.message import EmailMessage

def check_file(file):
    return os.path.getsize(file) > 0

def send_email(subject, body, to_email, from_email, password):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    # Connect to the server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.send_message(msg)
        print("Email sent successfully")

filepath = 'signals.txt'

to_email = 'songyuye29@gmail.com'
from_email = 'songyuye29@gmail.com'
password = 'qpkk fbdf mhtb gtoc'

if check_file(filepath):
    subject = 'Trading signals updated'
    body = ''
    send_email(subject, body, to_email, from_email, password)
else:
    print("No signals to send")