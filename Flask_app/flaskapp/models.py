from datetime import datetime
from flaskapp import db, login_manager
# __main__에서 가져올 필요없이 flaskapp에서 가져올 수 있다.
from flask_login import UserMixin

# @으로 데코레이터로 지정
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # 정확한 id가 들어오면 True를 반환합니다

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # int형 고유키 선언
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 유저 이름과 이메일은 글자수 제한(20, 120)이 있으며, 유니크하며, notnull 공백이 없습니다.
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # 유저의 프로필 사진으로 20자 길이의 해시값으로 이미지를 나타낸것입니다.
    # 기본사진을 사용할 수 있으므로 유니크는 삭제하고, 기본값을 설정해주겠습니다.
    password = db.Column(db.String(60), nullable=False)
    # 비밀번호 또한 60자의 해시값으로 나타낼것이고, 공백은 없습니다
    posts = db.relationship('Post', backref='author', lazy=True)
    # 한 유저가 여러 게시물을 작성할 수 는 있지만 한 게시물에는 하나의 작성자만 있을 수 있기때문에 backref로 관계설정
    # lazy 파라미터는 데이터 베이스를 불러오는 시기를 정할 수 있습니다. True일때는 필요한 데이터를 한번에 로드합니다.

    # 객체를 사용자가 이해할 수 있는 문자열로 반환하는 함수
    # https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 게시물이 작성된 날짜를 담는 열로 기본값은 datetime.utcnow로 뒤에 괄호를 붙이지 않은 이유는
    # 현재 시간이 아닌 데이터베이스에 저장할 때의 시간을 유지하기 위해서 입니다.
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 사용자 아이디를 외래키로 설정
    # 관계를 설정할때는 클래스의 이름을 Post 대문자 그대로 표현했지만 외래키를 설정할때는 user.id로 소문자로 바꿔서 표현했다.
    # 이는 외래키를 설정할때는 tablename을 가져와서, 관계를 설정할때는 클래스를 가져와서 대소문자가 바뀌는것이다.
    # 참고로 tablename을 따로 설정하지 않으면 class 이름에서 모두 소문자인 형태가 tablename이 된다.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coinname = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Post('{self.coinname}')"