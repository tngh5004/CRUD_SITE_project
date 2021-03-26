from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLALchemy
from forms import RegistrationForm, LoginForm
# forms.py 에서 Form 클래스들을 호출

app = Flask(__name__) 


app.config['SECRET_KEY'] = 'e89733e7694e28f0c3e4d79de2268d70'
# app에서 2가지 폼을 사용하기 위해 시크릿 키를 사용합니다.
# 시크릿 키는 쿠키 수정(cookie modify)과, 교차 사이트 요청 위조과 같은 간단한 해킹을 막아줍니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# ///은 상대경로이고, 위의 코드상 프로젝트 디렉토리에 site.db가 생성됩니다.

db = SQLAlchemy(app)
# 데이터베이스 인스턴스 생성

class User(db.Model):
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
    




post1 = [
    {
        'author': 'Sooho Kim',
        'title': 'Post 1',
        'content': 'First post content',
        'date_posted': 'March 23, 2021'
    },
    {
        'author': 'Jane Doe',
        'title': 'Post 2',
        'content': 'Second post content',
        'date_posted': 'March 25, 2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=post1)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
# register 페이지에서 발생하는 함수, 이 페이지에서는 get과 post 명령을 사용할 수 있음
def register():
    # register 페이지에 RegistrationForm() 클래스가 작동하게 만들어줌
    form = RegistrationForm()
    # 여기의 폼은 forms.py에서 선언한 Regist~~form이고,
    if form.validate_on_submit():
    # 만약 제출한 폼이 유효성 검사에 통과했다면 아래의 코드를 실행한다.
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
        # 유저 등록이 성공적으로 될시에 위와같은 일회성 문구를 전송하고, 홈페이지로 돌아갑니다.
    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    # 만약 제출한 폼이 유효성 검사에 통과했다면 아래의 코드를 실행한다.
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        # 데이터 베이스를 얻기 전까지 임시적인 방법입니다.
        # 만약 admin@blog.com으로 로그인 양식을 제출하고, password에 'password'를 입력한다면
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
# login 페이지에 LoginForm() 클래스가 작동하게 만들어줌


if __name__ == '__main__':
    app.run(debug=True)