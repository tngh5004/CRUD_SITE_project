from flask import render_template, flash, redirect, url_for, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.models import User, Post
# flaskapp 패키지에 모두 옮겼기 때문에 flaskapp.forms, flaskapp.models가 된다.
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # 여기의 폼은 forms.py에서 선언한 Regist~~form이고,
    if form.validate_on_submit():
        # 만약 제출한 폼이 유효성 검사에 통과했다면 아래의 코드를 실행한다.
        # form에 맞게 입력한 데이터를 User 클래스를 생성해서 데이터에 입력해줍니다.
        # 단 비밀번호는 해시화해서 넣어줍니다.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # db에 user 추가 후 커밋
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
        # 유저 등록이 성공적으로 될시에 위와같은 일회성 문구를 전송하고, 홈페이지로 돌아갑니다.
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
    # 만약 제출한 폼이 유효성 검사에 통과했다면 아래의 코드를 실행한다.
        user = User.query.filter_by(email=form.email.data).first()
        # email에 해당하는 데이터가 있다면 True를 반환
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # next_page가 있다면 next_page로 이동하고 아니면 홈페이지로 이동해라
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            # flash의 첫번째 인자는 메세지고, 두번째 인자는 success, danger등 정해진 메세지폼 입니다.
    return render_template('login.html', title='Login', form=form)
# login 페이지에 LoginForm() 클래스가 작동하게 만들어줌

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # static폴더의 profile_pics 디렉토리 안에 있는 유저의 이미지 파일
    return render_template('account.html', title='Account', image_file=image_file, form=form)
