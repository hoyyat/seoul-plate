import certifi

ca = certifi.where()

from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.akqwn.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SP'

import jwt
import datetime
import hashlib

@app.route('/')
def home():
    return render_template('log_in.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/detail')
def detail():
    plate_num = request.args.get('plate_num')
    # 게시글 사진, 이름, 위치, 메뉴
    plate = db.plates.find_one({'plate_num': int(plate_num)}, {'_id': False})
    # 게시글의 댓글
    comments = list(db.comments.find({'plate_num': str(plate_num)}, {'_id': False}))
    return render_template('detail.html', plate=plate, comments=comments)

@app.route('/main2')
def main2():
    plates = list(db.plates.find({}, {'_id': False}))
    comments = list(db.comments.find({}, {'_id': False}))
    return render_template('main2.html', plates=plates, comments=comments)

@app.route('/search')
def search():
    select = request.args.get('select') # url로 파라미터 받을때
    keyword = request.args.get('keyword')
    print(select, keyword)
    # select한 메뉴에 맞게 검색
    # '$regex' -> keyword가 포함하는 것 검색
    plates = list(db.plates.find({str(select): {'$regex':keyword}}, {'_id': False}))
    return render_template('search.html', plates=plates)

@app.route('/sp', methods=['GET'])
def sp_get():

    sp_list = list(db.plates.find({}, {'_id': False}))

    return jsonify({'sp_list': sp_list})

@app.route('/api/search', methods=['POST'])
def api_search():
    keyword_receive = request.form['keyword_give']

    search_list = list(db.plates.find({'place': keyword_receive}, {'_id': False}))

    return jsonify({'search_list': search_list})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    all_users = list(db.users.find({}, {'_id': False}))

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash
    }

    db.users.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '회원가입 성공!'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    # 아이디 중복체크
    exists = bool(db.users.find_one({"id": id_receive}))
    print(exists)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    # 아이디, 패스워드가 맞는지 확인
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/comment', methods=['POST'])
def api_comment():
    token_receive = request.cookies.get('mytoken')
    comment_receive = request.form['comment_give']
    plate_num = request.form['plate_num']

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})

        # 토큰을 활용하여 댓글 insert
        doc = {
            'id': user_info['id'],
            'comment': comment_receive,
            'plate_num': plate_num
        }

        db.comments.insert_one(doc)

        return jsonify({'msg': 'success'})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)