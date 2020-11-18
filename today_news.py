import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from my_project.Secret import clientid
from my_project.Secret import clientpw


client = MongoClient('localhost', 27017)
db = client.newscrap

def get_today_news(keyword):
    headers = {
        'X-Naver-Client-Id': clientid,
        'X-Naver-Client-Secret': clientpw,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    }

    params = {
        'query': keyword,
        'display': '100',
        'start': '1',
        'sort': 'sim',
    }

    response = requests.get('https://openapi.naver.com/v1/search/news.json', headers=headers, params=params)
    data = response.json()['items']


    for i in range(len(data)):
        data_url = requests.get(data[i]['link'], headers=headers)

        soup = BeautifulSoup(data_url.text, 'html.parser')
        try:
            image = soup.select_one('meta[property="og:image"]')['content']
        except TypeError:
            image = '이미지가 없습니다'
        print(data[i]['title'],data[i]['link'])
        print(image)
        data[i]['image'] = image
        data[i]['keyword'] = keyword

    for i in data:
        print(i)

    return data

def insert_today_news(data):
    client = MongoClient('localhost', 27017)
    db = client.newscrap
    db.main.insert_many(data)

def get_keyword_news(keyword):
    pass

data = get_today_news('카카오')
insert_today_news(data)


