import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

# Create a multipart message
msg = MIMEMultipart()
mf_link = 'http://www.mediafire.com/file/xza86n8ftpnneuj/arachni_1e82a339b6dae6aaa4c3c08f605456d5_scan_report.html.zip/file'
body_part = MIMEText('Test python scan report' + mf_link, 'plain')
msg['Subject'] = 'Python scan report'
msg['From'] = 'fypemail@yahoo.com'
msg['To'] = 'jasonling9199@gmail.com'
# Add body to email
msg.attach(body_part)

# Create SMTP object
session = smtplib.SMTP('smtp.mail.yahoo.com', 587)
session.starttls() #enable security
# Login to the server
session.login('fypemail@yahoo.com', 'driqnfsefylmmlwq')

# Convert the message to a string and send it
session.sendmail(msg['From'], msg['To'], msg.as_string())
print("Mail sent")
session.quit()

# sender_address = 'fypemail@yahoo.com'
# sender_pass = 'driqnfsefylmmlwq'
# receiver_address = 'jasonling9199@gmail.com'