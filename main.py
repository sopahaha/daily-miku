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


html = """\
<html>
  <body>
    <p>Hi, {name}<br>
      {text}</p>
    <img src="{image}"></img>
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
                formatedHtml = html.format(
                    name=name,
                    text=messages_json["daily_messages"][day_index],
                    image=messages_json["daily_images"][day_index])
                convertedHtml = MIMEText(formatedHtml, "html")
                message.attach(formatedHtml)

                print(formatedHtml)

                # server.sendmail(miku_email, email,
                #                 message.as_string())
                # sleep(4)
                print(f"Sent to {name}")
        print("Sent")
        messages_json["day_index"] += 1
        with open(MESSAGES_FILE, "w") as f:
            json.dump(messages_json, f)
        server.close()
except Exception as e:
    print(f"error: {e}")
