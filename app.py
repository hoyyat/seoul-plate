from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.akqwn.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SP'

import jwt
import datetime
import hashlib

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('log_in.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/sp', methods=['GET'])
def sp_get():
    sp_list = list(db.seoul.find({}, {'_id': False}).sort('title'))

    return jsonify({'sp_list': sp_list})

# @app.route('/api/detail')
# def api_detail():

@app.route('/api/search', methods=['POST'])
def api_search():
  keyword_receive = request.form['keyword_give']

  search_list = list(db.plates.find({'place': keyword_receive}, {'_id': False}).sort('title'))

  return jsonify({'search_list': search_list})

@app.route('/main')
def mainpage():
    return render_template('main page.html')


@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    all_users = list(db.users.find({}, {'_id': False}))

    for user in all_users:
        if user['id'] == id_receive:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디입니다.'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash
    }

    db.users.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '회원가입 성공!'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/comment', methods=['POST'])
def api_comment():
    token_receive = request.cookies.get('mytoken')
    comment_receive = request.form['comment_give']

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})

        doc = {
            'id': user_info['id'],
            'comment': comment_receive
        }

        db.comment.insert_one(doc)

        return jsonify({'msg': 'success'})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)