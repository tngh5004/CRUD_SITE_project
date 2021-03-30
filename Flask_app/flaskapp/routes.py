import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CoinForm
from flaskapp.models import User, Post, Coin
# flaskapp 패키지에 모두 옮겼기 때문에 flaskapp.forms, flaskapp.models가 된다.
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    post1 = Post.query.all()
    return render_template('home.html', posts=post1)

@app.route('/coin', methods=['GET', 'POST'])
@login_required
def coin():
    form = CoinForm()
    return render_template('coin.html', form=form)

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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # 사진의 크기를 125*125사이즈로 고정

    i.save(picture_path)
    # 사진의 경로는 앱의 루트경로와 패키지 디렉토리와 사진 파일 이름과 결합합니다.

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been uspdated!','success')
        return redirect(url_for('account'))
    # Update 폼 submit시에 유저의 이름과 이메일이 폼에 적은 이름과 이메일로 변경됨
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # 그냥 GET요청만 날린경우(일반적으로 입장한 경우) 폼에 현재 유저의 이름과 이메일을 보여줌
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # static폴더의 profile_pics 디렉토리 안에 있는 유저의 이미지 파일
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# CRUD
# CREATE
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # Post가 있으면 post id를 반환하고, 없으면 404를 반환해라
    return render_template('post.html', title=post.title, post=post)

#UPDATE
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
   
#DELETE
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))