import os
from flask import Flask, render_template, redirect, request, send_file, url_for, flash, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import socket
import time 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdsjhkFByukeafgsdyrdgj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
#home.html----------------------------------------------------------------------------------------------------------------
@app.route('/submit', methods=['POST'])
def submit():
    id = request.form.get('id')
    
    if id == "buy_gbl":
        return redirect('https://youtu.be/UIp6_0kct_U')
    
    elif id == "download_mc_mod":
        return render_template('download_mod.html')
    
    elif id == "dlmcmodac":
        return render_template('home.html')
                
    else:
        return render_template('404.html')

#download_mod.html--------------------------------------------------------------------------------------------------------
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    try:
        # 獲取當前腳本的目錄
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # 構建絕對路徑
        file_path = "D:/py/EA1copy/app2/static/mods.zip"
        
        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            return render_template('404.html')
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        return str(e)
#檢查指定的Minecraft伺服器是否在線

def is_minecraft_server_online(ip, port=25565):
    try:
        time.sleep(5)
        with socket.create_connection((ip, port), timeout=10):
            return True
    except OSError:
        return False

@app.route('/check_server_status')
@login_required
def check_server_status():
    ip = "192.168.0.230"
    if is_minecraft_server_online(ip):
        return jsonify(status='online')
    else:
        return jsonify(status='offline')




