from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.newscrap

app = Flask(__name__)

def is_email(email):
    find_email = list(db.email.find({'email': email}))
    if not find_email:
        return False
    else:
        return True

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/news/list', methods=['GET'])
def show_news():
    news = list(db.main.find({},{'_id':False}).sort('_id',-1).limit(10))
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!', 'news':news})

@app.route('/email/save', methods=['POST'])
def email_insert():
    email = request.form['email']
    keywords = request.form['keywords']

    if is_email(email):
        return jsonify({'result': 'success', 'msg': '이미 구독하셨습니다'})
    else:
        doc = {
            'email': email,
            'keywords': keywords
        }
        db.email.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '완료되었습니다'})

@app.route('/email/del', methods=['POST'])
def email_delete():
    email = request.form['email']
    if is_email(email):
        db.email.delete_one({'email': email})
        return jsonify({'result': 'success', 'msg': '삭제되었습니다'})
    else:
        return jsonify({'result': 'success', 'msg': '구독하지 않은 이메일입니다'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
