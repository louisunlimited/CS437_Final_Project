import smtplib
from email.mime.text import MIMEText

subject = "Warning Email"
body = "Call 911 or die"
sender = "cproject267@gmail.com"
recipients = [" cproject267@gmail.com"]
password = "ibry eynm sjkj qogk" #App password, SMTP may fail if this is not the riht app passsword. Need to generate an app password for each new device.


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, body, sender, recipients, password)

