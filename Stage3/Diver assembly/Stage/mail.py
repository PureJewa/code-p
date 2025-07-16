# Import smtplib for the actual sending function
import smtplib
me = 'j.vandewater@code-p.nl'
you = 'jelle.van.de.water@hotmail.nl'
# Import the email modules we'll need
from email.message import EmailMessage
textfile = 'mail.txt'
# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of {textfile}'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP(me)
s.send_message(msg)
s.quit()