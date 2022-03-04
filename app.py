import uuid
from flask import Flask, redirect, request, url_for
from flask import render_template
from flask_login import LoginManager, current_user, login_required, login_user

from api import *

app = Flask(__name__)

app.secret_key = 'secret_rianng.cn_8023_{}'.format(uuid.uuid1())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    emsg = None
    if form.validate_on_submit():
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        user_info = get_user(username)
        if user_info is None:
            if password1 == password2:
                create_user(username, password1)
                return redirect(url_for('login'))
            else:
                emsg = 'Different password.'
        else:
            emsg = 'Username exists.'
    return render_template('register.html', form=form, emsg=emsg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_info = get_user(username)
        if user_info is None:
            emsg = 'Wrong username or password.'
        else:
            user = User(user_info)
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = 'Wrong username or password.'
    return render_template('login.html', form=form, emsg=emsg)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    a_config = ada_config()
    
    user = User(current_user)
    accs_token = user.get_accs_token()

    accs_info = []
    for acc_token in accs_token:
        a_api = ada_api(acc_token, only_read=True)
        acc_info = a_api.get_account_info()
        accs_info.append(acc_info)
    if request.method == 'GET':
        return render_template('index.html', accounts=accs_info)
    else:
        token = request.form.get('token')
        a_api = ada_api(token, only_read=True)
        if a_api.account is not None:
            acc_info = a_api.get_account_info()
            return render_template('index.html', accounts=accs_info, new_acc_info=acc_info)
        else:
            return render_template('index.html', accounts=accs_info, new_acc_info={'None': token})

@app.route('/api/acc/add', methods=['POST'])
@login_required
def add_acc():
    token = request.form.get('token')
    a_config = ada_config()
    a_api = ada_api(token)
    acc_info = a_api.get_account_info()
    user = User(current_user)
    user.add_acc(acc_info['uid'])
    return redirect('/')

@app.route('/analyze/refresh', methods=['POST'])
@login_required
def refresh_ada():
    token = request.form.get('token')
    a_api = ada_api(token)
    return redirect('/')

@app.route('/analyze/refresh/force', methods=['POST'])
@login_required
def refresh_force_ada():
    token = request.form.get('token')
    a_api = ada_api(token, force_refresh=True)
    return redirect('/')

@app.route('/analyze', methods=['POST'])
@login_required
def analyze_results():
    token = request.form.get('token')
    a_config = ada_config()

    user = User(current_user)
    accs_token = user.get_accs_token()

    accs_info = []
    for acc_token in accs_token:
        a_api = ada_api(acc_token, only_read=True)
        acc_info = a_api.get_account_info()
        accs_info.append(acc_info)
    a_api = ada_api(token, only_read=True)
    a_info = a_api.get_all_info()
    return render_template('analysis.html', info=a_info, accounts=accs_info)

if __name__ == '__main__':
    app.run(debug=True, port=8900)
