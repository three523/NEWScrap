from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from my_project.check_mail import check_sendmail
import numpy as np

client = MongoClient('localhost', 27017)
db = client.newscrap

app = Flask(__name__)

def rand_cd():
    random = []
    for i in range(10):
        random.append(str(np.random.randint(10)))
    random = "".join(random)
    return random

def is_email(email):
    find_email = list(db.sender.find({'email': email}))
    if not find_email:
        return False
    else:
        return True

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/news/list', methods=['GET'])
def show_news():
    news = list(db.main.find({},{'_id':False}).sort('_id',-1).limit(28))
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!', 'news':news})

@app.route('/email/save', methods=['POST'])
def email_insert():
    email = request.form['email']
    keywords = request.form['keywords']

    if is_email(email):
        return jsonify({'result': 'success', 'msg': '이미 구독하셨습니다'})
    else:

        db.email.update_one({'email': email}, {'$set': {'keywords': keywords, 'randCD':rand_cd()}}, upsert=True)
        check_sendmail(email)
        # return jsonify({'result': 'success', 'msg': f'{email}로 이메일을 보냈습니다. 이메일을 확인하고 인증해 주세요', 'id':email})
        return render_template('ischeck.html',myemail=email)

@app.route('/email/del', methods=['POST'])
def email_delete():
    email = request.form['email']
    if is_email(email):
        db.email.delete_one({'email': email})
        db.sender.delete_one({'email': email})
        return jsonify({'result': 'success', 'msg': '삭제되었습니다'})
    else:
        return jsonify({'result': 'success', 'msg': '구독하지 않은 이메일입니다'})

@app.route('/ismail', methods=['GET'])
def test():
    return render_template('ischeck.html')

@app.route('/resend', methods=["POST"])
def re_send():
    email = request.form['email']
    db.email.updateOne({'email':email},{'$set' :{'randCD':rand_cd()}})
    check_sendmail(email)
    return jsonify({'result': 'success', 'msg': '다시 발송하였습니다'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
