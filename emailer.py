import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import time
import pathlib
import dropbox
import re

## HARDCODED FILE PATH, CHANGE THIS LATER
# the source file
folder = pathlib.Path("./reports/")    # located in this folder
scanID = "f1247dfee641c1a7ed953f5770bfd144"
filename = scanID + ".html.zip"         # file name
filepath = folder / filename  # path object, defining the file

# target location in Dropbox
target = "/"              # the target folder
targetfile = target + filename   # the target path and file name

# Create a dropbox object using an API v2 key
d = dropbox.Dropbox("ClkPn4pV_5sAAAAAAAAAAUm4ft1qOk4VNd77wioArPu7WbFxQBb1f7-UKZQPfaRB")

# open the file and upload it
with filepath.open("rb") as f:
   # upload gives you metadata about the file
   # we want to overwite any previous version of the file
   meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))

# create a shared link
link = d.sharing_create_shared_link(targetfile)

# url which can be shared
dropbox_url = link.url

print(dropbox_url)

#take scan id, call mediafire uploader and then get dl link to email to user
time.sleep(10)
# Create a multipart message
msg = MIMEMultipart()
body_part = MIMEText('Your report is ready, here is the link to download it: ' + dropbox_url, 'plain')
msg['Subject'] = 'Python scan report'
msg['From'] = 'fypemail@yahoo.com' #change this to email used by us
msg['To'] = 'jasonling9199@gmail.com' #change this to email input from user
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
session.quit() #closes email session after done

# sender_address = 'fypemail@yahoo.com'
# sender_pass = 'driqnfsefylmmlwq'
# receiver_address = 'jasonling9199@gmail.com'