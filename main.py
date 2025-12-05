import smtplib
import ssl
import csv
import os
import json
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

MESSAGES_FILE = "messages.json"

with open(MESSAGES_FILE, "r") as f:
    messages_json = json.load(f)

day_index = messages_json['day_index']

port = 465
smtp_server = "smtp.gmail.com"
miku_email = os.getenv('EMAIL_ADDR')
receiver_email = "vitorcesarino1@gmail.com"
miku_password = os.getenv('EMAIL_PASSWORD')


html = f"""\
<html>
  <body>
    <p>Hi, {{name}}<br>
      {messages_json["daily_messages"][day_index]}</p>
    <img src="{messages_json["daily_images"][day_index]}"></img>
  </body>
</html>
"""


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
                message = MIMEMultipart("alternative")
                message["Subject"] = "Daily miku for you"
                message["From"] = miku_email
                formatedHtml = html.format(name=name)
                convertedHtml = MIMEText(formatedHtml, "html")
                message.attach(convertedHtml)

                server.sendmail(miku_email, email,
                                message.as_string())
                print(f"Sent to {name}")
                sleep(4)
        print("Sent")
        messages_json["day_index"] += 1
        with open(MESSAGES_FILE, "w") as f:
            json.dump(messages_json, f)
        server.close()
except Exception as e:
    print(f"error: {e}")
