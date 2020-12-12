import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from my_project.Secret import mailid
from my_project.Secret import mailpw
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.newscrap

def check_sendmail(receiver):
    check_code = db.email.find_one({'email':receiver},{'randCD':True, '_id': False})
    check_code = check_code['randCD']

    sender = mailid
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(mailid, mailpw)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Newscrap'
    msg['To'] = receiver
    msg['From'] = sender

    html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
            <hr size="5px" color="darkgray" width="90%">
            <div style="display: flex; justify-content: center; align-items: center; flex-direction: column">
                <h1 style="font-size: 50px">Newscrap</h1>
                <div class="content" style=" width:100%; padding:40px 0; background-color:#ffffff;margin:0 auto;">
                    <div id="test" cellpadding="0" cellspacing="0"
                           style="display: flex; justify-content: center; align-items: center; flex-direction: column; margin: 0px auto; width: 94%; max-width: 630px; border: 0px;">
                        <img src="static/email_open.png" alt="" width="100px" height="100px" style="margin: 10px 0">
                        <p style="display: flex; font-size: xx-large; width: 100%; padding-left: 5px; margin-bottom: 50px" ><strong style="margin-right: 5px">메일인증</strong> 안내입니다</p>
                        <p style="margin: 10px 0; width: 100%">Newscrap을 이용해주셔서 감사합니다<br>
                                                     아래의 코드를<br>
                                                     인증하기 버튼을 클릭하여 들어가 입력해주시기 바랍니다</p>
                        <div style="width: 100%; margin: 20px; text-align: center; background-color: darkgrey">
                            <strong style="font-size: 50px;">{check_code}</strong>
                        </div>
                        <a href="http://localhost:5000/ismail" style=" display:flex; justify-content: center; align-items: center; width: 400px; height: 80px; background-color: black; color: white; font-size: x-large; text-decoration:none;">인증하러가기</a>
                    </div>
                </div>
            </div>
            <hr size="5px" color="darkgray" width="90%">
            </body>
            </html>
            '''

    part = MIMEText(html, 'html')
    msg.attach(part)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()