from flask import Flask
from flask import render_template

from api import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Arknights Data Analysis</p>'

@app.route('/analyze/')
@app.route('/analyze/<token>')
def analyze_results(token=None):
    a_config = ada_config()
    accounts_config = a_config.load_config_accounts()
    accs_info = []
    for acc_config in accounts_config:
        a_api = ada_api(acc_config['token'], only_read=True)
        acc_info = a_api.get_account_info()
        accs_info.append(acc_info)
    a_api = ada_api(token, only_read=True)
    a_info = a_api.get_all_info()
    print(a_info)
    return render_template('analysis.html', info=a_info, accounts=accs_info)

if __name__ == '__main__':
    app.run(debug=True, port=8900)
