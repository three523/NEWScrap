from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from my_project.check_mail import check_sendmail
import string
import random

client = MongoClient('localhost', 27017)
db = client.newscrap

app = Flask(__name__)

def rand_cd():
    string_rand = string.ascii_letters + string.digits
    result = ''
    for i in range(10):
        result += random.choice(string_rand)
    return result

def is_email(email):
    find_email = list(db.sender.find({'email': email}))
    if not find_email:
        return False
    else:
        return True

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/email/save', methods=['POST'])
def email_insert():
    email = request.form['email']
    keywords = request.form['keywords']

    if is_email(email):
        return jsonify({'result': False, 'msg': '이미 구독하셨습니다'})
    else:
        db.email.update_one({'email': email}, {'$set': {'keywords': keywords, 'randCD':rand_cd()}}, upsert=True)
        check_sendmail(email)
        return render_template('ischeck.html',myemail=email)

@app.route('/email/del', methods=['POST'])
def email_delete():
    email = request.form['email']
    if is_email(email):
        db.email.delete_one({'email': email})
        db.sender.delete_one({'email': email})
        return jsonify({'result': 'success', 'msg': '삭제되었습니다'})
    else:
        db.sender.insert_one({})
        return jsonify({'result': 'success', 'msg': '구독하지 않은 이메일입니다'})

@app.route('/email/code', methods=['POST'])
def email_code():
    usercd = request.form['code']
    is_user = db.email.find_one({'randCD': usercd})
    if not is_user:
        return jsonify({'result': False, 'msg': '인증코드가 잘못돠었습니다'})
    else:
        db.sender.insert_one({'email': is_user['email'],
                             'keywords': is_user['keywords']})
        db.email.delete_one({'email':is_user['email']})
        return jsonify({'result': True, 'msg': '구독이 완료되었습니다'})

@app.route('/resend', methods=["POST"])
def re_send():
    email = request.form['email']
    db.email.update_one({'email':email},{'$set' :{'randCD':rand_cd()}})
    print(email)
    check_sendmail(email)
    return jsonify({'msg': '다시 발송하였습니다'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
