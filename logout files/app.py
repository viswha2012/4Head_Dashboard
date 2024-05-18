from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session
from requests_html import HTMLSession
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user
import pandas as pd
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AMZTKgwfadRRjrcMyPdiaTYsJTMMuTJz@viaduct.proxy.rlwy.net:18329/railway'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

API_TOKEN = "5241e6a8-7a00-4900-ba53-06f8534b88ac"
API_SECRET = "fa5b8d414716f8ebc108de54e84967ffd4e92e76bb2983b342cb494feacc258c"

DASHBOARD_ID_C = "8ddb3ada-daf5-49ba-952c-b4b17bbb8961"
DASHBOARD_ID_P = "b790a00c-d039-4672-a358-f914bfa4985a"
DASHBOARD_ID_I = "c24117c3-db17-4c8b-b6d5-6569e3552ac4"
DASHBOARD_ID_D = "8f0249ef-7c08-472d-a1c9-08187cb8fb36"

SUPERSET_DOMAIN = "https://f884644f.us1a.app.preset.io"
PRESET_TEAM = "23a09e83"
WORKSPACE_SLUG = "f884644f"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = 'Police_deets'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(50))
    fullname = db.Column(db.String(50))
 

ssession = HTMLSession()
url = "https://news.google.com/rss/search?q=Karnataka Crime Police"
r = ssession.get(url)

titles = []

for title in r.html.find('title'):
    titles.append(title.text)
    if len(titles) >= 8:
        break

titles = titles[1:]

def load_work_data():
    try:
        data = pd.read_excel("data.xlsx", engine="openpyxl").to_dict(orient="records")
    except FileNotFoundError:
        data = []
    return data

def save_work_data(data):
    df = pd.DataFrame(data)
    df.to_excel("data.xlsx", index=False, engine="openpyxl")

@app.route('/')
def login():
    return render_template('login.html')

@app.route("/guest-token", methods=["GET"])
def guest_token():
    dashboard_id = request.args.get("dashboard_id")
    print("Dashboard ID:", dashboard_id)

    url = "https://manage.app.preset.io/api/v1/auth/"
    payload = json.dumps({
        "name": API_TOKEN,
        "secret": API_SECRET
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response1 = requests.request("POST", url, headers=headers, data=payload)
    preset_access_token = json.loads(response1.text)['payload']['access_token']
    print("Preset Access Token:", preset_access_token)

    payload = json.dumps({
        "user": {
            "username": "LukeSky",
            "first_name": "Luke",
            "last_name": "Skywalker"
        },
        "resources": [{
            "type": "dashboard",
            "id": dashboard_id
        }],
        "rls": []
    })
    print("Payload:", payload)
    bearer_token = "Bearer " + preset_access_token
    response2 = requests.post(
        "https://manage.app.preset.io/api/v1/teams/23a09e83/workspaces/f884644f/guest-token/",
        data=payload,
        headers={"Authorization": bearer_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    )
    return jsonify(response2.json()['payload']['token'])



@app.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    details = User.query.filter_by(username=username).first()
    if details:
        if details.password == password:
            session['role'] = details.role
            session['fullname'] = details.fullname
            return redirect('/central')
    
    return 'Invalid username or password. Please try again.'

"""@app.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    if username=="viswha":
        if password == "1234":
            session['role'] = "precinct"
            session['fullname'] = "viswha vijay"
            return redirect('/central')
    
    return 'Invalid username or password. Please try again.'"""


@app.route("/central")
def central():
    name = session.get('fullname').upper()
    return render_template("central.html" , titles=titles, name = name)

@app.route("/route")
def routef():
    work_data = load_work_data()
    role = session.get('role')
    name = session.get('fullname').upper()
    route_html = role + ".html"
    try:
        data = pd.read_excel('data.xlsx')
    except FileNotFoundError:
        data = pd.DataFrame()

    data = data[::-1]
    return render_template(route_html, data=data, name = name, work_data=work_data)

@app.route('/submit_concern', methods=['POST'])
def submit():
     data = request.json.get('input_data')
     data = session.get('fullname') + ":  " + data
     try:
        existing_data = pd.read_excel('data.xlsx')
     except FileNotFoundError:
        existing_data = pd.DataFrame()

     new_data = pd.DataFrame({'Data': [data]})
     updated_data = pd.concat([existing_data, new_data], ignore_index=True)

     updated_data.to_excel('data.xlsx', index=False)
     return 'Concern submitted successfully', 'success'

@app.route('/submit_work', methods=['POST'])
def submit_work():
    work_assigned_by = request.form['work_assigned_by']
    work_assigned_to = request.form['work_assigned_to']
    task = request.form['task']
    deadline = request.form['deadline']
    new_row = {"Work Assigned By": work_assigned_by, "Work Assigned To": work_assigned_to, "Task": task, "Deadline": deadline}
    data = load_work_data()
    data.append(new_row)
    save_work_data(data)
    return redirect(request.referrer)

@app.route('/delete_work/<int:index>')
def delete_work(index): 
    data = load_work_data()
    del data[index]
    save_work_data(data)
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=True)