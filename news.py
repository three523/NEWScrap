import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from my_project.Secret import clientid
from my_project.Secret import clientpw

client = MongoClient('localhost', 27017)
db = client.newscrap

def get_email_news(email_keyowrds):
    headers = {
        'X-Naver-Client-Id': clientid,
        'X-Naver-Client-Secret': clientpw,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    for email_keyowrd in email_keyowrds:
        keywords = email_keyowrd['keywords'].split(',')
        datas = []
        for i in range(len(keywords)-1):
            print(keywords[i])
            params = {
                'query': keywords[i],
                'display': '8',
                'start': '1',
                'sort': 'sim',
            }

            response = requests.get('https://openapi.naver.com/v1/search/news.json', headers=headers, params=params)
            datas.append(response.json()['items'])
            datas[i][0]['keyword'] = keywords[i]

        for data in datas:
            for i in range(len(data)):
                print(data[i])
                data_url = requests.get(data[i]['link'], headers=headers)
                soup = BeautifulSoup(data_url.text, 'html.parser')
                try:
                    image = soup.select_one('meta[property="og:image"]')['content']
                except TypeError:
                    image = '이미지가 없습니다'
                data[i]['image'] = image
                data[i]['keyword'] = data[0]['keyword']

        mail_sender = {'email': email_keyowrd['email'], 'news': datas}
        db.sender.update_one({'email': email_keyowrd['email']}, {'$set': mail_sender}, upsert=True)

def get_keyword_news():
    keywords = list(db.sender.find({},{'_id':False}))
    return keywords

keywords = get_keyword_news()
print(keywords)
get_email_news(keywords)
