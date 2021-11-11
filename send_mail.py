import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_mail(secrets, subject, message, files=[]):
    msg = MIMEMultipart()
    msg['From'] = secrets['from']
    msg['To'] = secrets['to']
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    use_tls = True
    port = 587
    smtp = smtplib.SMTP( secrets['server'], port)
    if use_tls:
        smtp.starttls()
    smtp.login(secrets['username'], secrets['password'])
    smtp.sendmail(secrets['from'], secrets['to'], msg.as_string())
    smtp.quit()

