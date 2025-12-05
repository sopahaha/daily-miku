import smtplib
import ssl
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

port = 465
smtp_server = "smtp.gmail.com"
miku_email = os.getenv('EMAIL_ADDR')
receiver_email = "vitorcesarino1@gmail.com"
miku_password = os.getenv('EMAIL_PASSWORD')

message = MIMEMultipart("alternative")
message["Subject"] = "Daily miku for you"
message["From"] = miku_email

html = """\
<html>
  <body>
    <p>Hi, {name}<br>
      Check out the new miku on your mail:</p>
    <img src="https://c.tenor.com/rUkr3PJaIHAAAAAd/tenor.gif"></img>
  </body>
</html>
"""

convertedHtml = MIMEText(html, "html")
message.attach(convertedHtml)

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("Authenticating...")
        server.login(miku_email, miku_password)
        print("Sending mails...")
        with open("emails.csv") as file:
            reader = csv.reader(file)
            next(reader)
            for email, name in reader:
                server.sendmail(miku_email, email,
                                message.as_string().format(name=name))
                print(f"Sent to {name}")

        print("Sent")
        server.close()
except Exception as e:
    print(f"error: {e}")
