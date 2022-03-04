import uuid
from flask import Flask, redirect, request
from flask import render_template
from flask_login import LoginManager

from api import *

app = Flask(__name__)

app.secret_key = 'secret_rianng.cn_8023_{}'.format(uuid.uuid1())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/', methods=['GET', 'POST'])
def index():
    a_config = ada_config()
    accounts_config = a_config.load_config_accounts()
    accs_info = []
    for acc_config in accounts_config:
        a_api = ada_api(acc_config['token'], only_read=True)
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
def add_acc():
    token = request.form.get('token')
    a_config = ada_config()
    a_api = ada_api(token)
    acc_info = a_api.get_account_info()
    a_config.add_config_account(acc_info['nickName'], token)
    
    return redirect('/')

@app.route('/analyze/refresh', methods=['POST'])
def refresh_ada():
    token = request.form.get('token')
    a_api = ada_api(token)
    return redirect('/')

@app.route('/analyze/refresh/force', methods=['POST'])
def refresh_force_ada():
    token = request.form.get('token')
    a_api = ada_api(token, force_refresh=True)
    return redirect('/')

@app.route('/analyze', methods=['POST'])
def analyze_results():
    token = request.form.get('token')
    a_config = ada_config()
    accounts_config = a_config.load_config_accounts()
    accs_info = []
    for acc_config in accounts_config:
        a_api = ada_api(acc_config['token'], only_read=True)
        acc_info = a_api.get_account_info()
        accs_info.append(acc_info)
    a_api = ada_api(token, only_read=True)
    a_info = a_api.get_all_info()
    return render_template('analysis.html', info=a_info, accounts=accs_info)

if __name__ == '__main__':
    app.run(debug=True, port=8900)
