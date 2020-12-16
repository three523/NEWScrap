import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from my_project.Secret import mailid
from my_project.Secret import mailpw
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.newscrap

def user_sendMail(sender, receiver, news_list):
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
            <div class="wrap">
                <div class="content" style=" width:100%; padding:40px 0; background-color:#ffffff;margin:0 auto; background: rgb(235, 235, 235);">
                    <table id="test" cellpadding="0" cellspacing="0" align="center"
                           style=" margin: 0px auto; width: 94%; max-width: 630px; background: rgb(235, 235, 235); border: 0px;">
                        <tr style="margin: 0;padding:0;">
                            <h1 style="display: flex; justify-content: center; font-size: 80px">NewScrap</h1>
                        </tr>
    '''
    for news in news_list:
        for i in range(0,len(news),2):
            if i != 0:
                html += f'''
                <tr style="display: flex; margin: 0;padding:0;">
                    <td style="width: 100%; max-width: 630px; margin: 0 auto; position: relative; border-spacing: 0; clear: both; border-collapse: separate;padding:0;overflow:hidden;_width:620px;">
                        <a href="{news[i]["link"]}">
                            <img src="{news[i]["image"]}" alt=""
                                 style="width: 100%; height: 40%; max-height: 200px; display: inline; vertical-align: middle; max-width: 100%; border-width: 0px; border-color: initial; border-image: initial; text-align: justify;"
                                 width="610">
                            <h1>{news[i]["title"]}</h1>
                            <h2>{news[i]["description"]}</h2>
                        </a>
                    </td>
                    <td style="width: 100%; max-width: 630px; margin: 0 auto; position: relative; border-spacing: 0; clear: both; border-collapse: separate;padding:0;overflow:hidden;_width:620px;">
                        <a href="{news[i+1]["link"]}">
                            <img src="{news[i+1]["image"]}" alt=""
                                 style="width: 100%; height: 40%; max-height: 200px; display: inline; vertical-align: middle; max-width: 100%; border-width: 0px; border-color: initial; border-image: initial; text-align: justify;"
                                 width="610">
                            <h1>{news[i+1]["title"]}</h1>
                            <h2>{news[i+1]["description"]}</h2>
                        </a>
                    </td>
                </tr>'''
            elif i == 0:
                html += f'''
                <td style="margin: 0;padding:0;">
                    <h1 style="display: flex; border-bottom: 1px solid black; font-size: 40px">{news[i]["keyword"]}</h1>
                </td>
                <tr style="display: flex; margin: 0;padding:0;">
                    <td style="width: 100%; max-width: 630px; margin: 0 auto; position: relative; border-spacing: 0; clear: both; border-collapse: separate;padding:0;overflow:hidden;_width:620px;">
                        <a href="{news[i]["link"]}">
                            <img src="{news[i]["image"]}" alt=""
                                 style="width: 100%; height: 40%; max-height: 200px; display: inline; vertical-align: middle; max-width: 100%; border-width: 0px; border-color: initial; border-image: initial; text-align: justify;"
                                 width="610">
                            <h1>{news[i]["title"]}</h1>
                            <h2>{news[i]["description"]}</h2>
                        </a>
                    </td>
                    <td style="width: 100%; max-width: 630px; margin: 0 auto; position: relative; border-spacing: 0; clear: both; border-collapse: separate;padding:0;overflow:hidden;_width:620px;">
                        <a href="{news[i+1]["link"]}">
                            <img src="{news[i+1]["image"]}" alt=""
                                 style="width: 100%; height: 40%; max-height: 200px; display: inline; vertical-align: middle; max-width: 100%; border-width: 0px; border-color: initial; border-image: initial; text-align: justify;"
                                 width="610">
                            <h1>{news[i+1]["title"]}</h1>
                            <h2>{news[i+1]["description"]}</h2>
                        </a>
                    </td>
                </tr>'''
    html += '''
                        </table>
                    </div>
                </div>
            </body>
            </html>'''

    part = MIMEText(html, 'html')
    msg.attach(part)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

users = list(db.sender.find({},{'_id':False}))

for user in users:
    user_sendMail(mailid, user['email'], user['news'])
