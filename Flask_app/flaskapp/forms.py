from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# 문자열, 비밀번호, 제출, 제약조건 을 위한 필드
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# 유효성 검사기 : 데이터의 유무, 글자수, 이메일, 동일성 확인
from flaskapp.models import User

# FlaskForm에 상속되는 클래스 생성
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)]) 
    # 유저는 문자열 필드로 선언하고, 이름은 Username
    # 제한사항 : 공백금지, 글자수 제한(2~20)
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    # 제한사항 : 공백금지, 유효한 이메일
    
    password = PasswordField('Password', validators=[DataRequired()]) 
    # 제한사항 : 공백금지
    
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # 제한사항 : 공백금지, 비밀번호와 같아야됨
    
    submit = SubmitField('Sing Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

# 로그인 양식, 등록 양식에서 조금만 수정해주면 된다.
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 유저이름은 잘 잊어먹으므로 이메일을 로그인 양식으로 사용할것입니다.
    
    password = PasswordField('Password', validators=[DataRequired()]) 
    # 비밀번호를 확인하는 파트는 필요없어집니다.
    
    remember = BooleanField('Remeber Me')
    # 제약조건을 통한 로그인 유지
    
    submit = SubmitField('Login')
    # 로그인


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)]) 
    # 유저는 문자열 필드로 선언하고, 이름은 Username
    # 제한사항 : 공백금지, 글자수 제한(2~20)
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    # 제한사항 : 공백금지, 유효한 이메일
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')