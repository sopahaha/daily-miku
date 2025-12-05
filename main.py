import smtplib
import ssl
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

port = 465
smtp_server = "smtp.gmail.com"
miku_email = os.getenv('EMAIL_ADDR')
receiver_email = "vitorcesarino1@gmail.com"
miku_password = os.getenv('EMAIL_PASSWORD')

message = MIMEMultipart("alternative")
message["Subject"] = "Multipart test"
message["From"] = miku_email
message["To"] = receiver_email

html = """\
<html>
  <body>
    <p>Hi,<br>
      Check out the new miku on your mail:</p>
    <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia1.tenor.com%2Fm%2FwTFUTy-YBTsAAAAC%2Fmiku-hatsune-miku.gif&f=1&nofb=1&ipt=ac05c37441f15f0277c5f236de41d3e52a14e9688957d670e0d25d624acbff61"></img>
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
        print("Sending mail...")
        server.sendmail(miku_email, receiver_email, message.as_string())
        print("Sent")
        server.close()
except Exception as e:
    print(f"error: {e}")
