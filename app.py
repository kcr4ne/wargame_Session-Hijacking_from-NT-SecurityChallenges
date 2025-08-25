#!/usr/bin/python3
from flask import Flask, request, render_template, make_response, redirect, url_for
import os

app = Flask(__name__)

with open('./flag.txt', 'r') as f:
    FLAG = f.read()

users = {
    'user': 'user',
    'admin': os.urandom(16).hex()
}

# this is our session storage
storage = {
}

# 서버 시작 시 admin 세션 ID를 생성하고 저장합니다.
# 이 값은 전역 변수로 저장되어 index() 함수에서 접근 가능합니다.
admin_session_id = os.urandom(16).hex()
storage[admin_session_id] = 'admin'


@app.route('/')
def index():
    session_id = request.cookies.get('sessionid', None)
    
    # admin의 세션 ID를 템플릿으로 전달합니다.
    # 이 부분이 바로 취약점을 노출하는 지점입니다.
    leaked_admin_session = f"어드민의 세션 아이디가 떨어져 있네요? -> {admin_session_id}"

    try:
        name = storage[session_id]
    except KeyError:
        return render_template('index.html', text="로그인 해주세요.", admin_info=leaked_admin_session)

    return render_template('index.html', text=f'{FLAG if name == "admin" else "어드민만 접근 가능"}', admin_info=leaked_admin_session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        resp = make_response(render_template('login.html'))
        if not request.cookies.get('sessionid'):
            session_id = os.urandom(16).hex()
            resp.set_cookie('sessionid', session_id)
        return resp
    
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            pw = users[username]
        except:
            return '<script>alert("해당 유저 계정이 없습니다.");history.go(-1);</script>'

        if pw == password:
            session_id = request.cookies.get('sessionid')
            storage[session_id] = username
            return redirect(url_for('index'))
        
        return '<script>alert("패스워드가 일치하지 않습니다.");history.go(-1);</script>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2003)