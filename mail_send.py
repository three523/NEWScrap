import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from my_project.Secret import mailid
from my_project.Secret import mailpw



def sendMail(me, you):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(mailid, mailpw)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'TEST'
    msg['To'] = you
    msg['From'] = 'Newscrap'

    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """

    part = MIMEText(html, 'html')
    
    msg.attach(part)

    smtp.sendmail(me, you, msg.as_string())
    smtp.quit()

sendMail('thtree523@gmail.com', 'nadoji304@naver.com')
