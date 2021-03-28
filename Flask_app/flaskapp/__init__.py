from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__) 

app.config['SECRET_KEY'] = 'e89733e7694e28f0c3e4d79de2268d70'
# app에서 2가지 폼을 사용하기 위해 시크릿 키를 사용합니다.
# 시크릿 키는 쿠키 수정(cookie modify)과, 교차 사이트 요청 위조과 같은 간단한 해킹을 막아줍니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# ///은 상대경로이고, 위의 코드상 프로젝트 디렉토리에 site.db가 생성됩니다.

db = SQLAlchemy(app)
# 데이터베이스 인스턴스 생성
bcrypt = Bcrypt(app)
# 비밀번호 해쉬화
login_manager = LoginManager(app)
# 로그인 매니저
login_manager.login_view = 'login'
# 인자인 login은 경로의 함수 이름
login_manager.login_message_category = 'info'

from flaskapp import routes
# impoort 순환오류를 방지하기 위해 아래에서 import