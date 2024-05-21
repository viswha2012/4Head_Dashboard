from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session
from requests_html import HTMLSession
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user
import pandas as pd
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:IePdnhHQTMYuLZdacSUSfuidTltQauIP@roundhouse.proxy.rlwy.net:34416/railway'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

API_TOKEN = "f318e285-9792-4f0f-9c90-398a5d7a3c0d"
API_SECRET = "cbbf40431893fb22211c09722bc0df319612c97bb9af1869222bfe478b1ad5dc"

DASHBOARD_ID_C = "0596b651-13e7-4e09-9f9c-acf78ff96374"
DASHBOARD_ID_P = "45818bbc-bf51-40c5-a84b-3a57e3f613cd"
DASHBOARD_ID_I = "a3937c4c-e78f-469c-915d-276f9fbd92f8"
DASHBOARD_ID_D = "1255f209-4d57-4ea3-86e0-26edcc456f49"

SUPERSET_DOMAIN = "https://1296954c.us1a.app.preset.io"
PRESET_TEAM = "ce7d1299"
WORKSPACE_SLUG = "1296954c"


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

    def __init__(self, id, username, password, role, fullname):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.fullname = fullname
 

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
        "https://manage.app.preset.io/api/v1/teams/ce7d1299/workspaces/1296954c/guest-token/",
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
            if session['role']=='register':
                return redirect('/register') 
            else:
                return redirect('/central') 
            
    flash("Invalid username or password. Please try again.")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # Redirect to the login page

@app.route("/register")
def register():
        return render_template("register.html")

@app.route("/upload", methods=["GET", "POST"])
def postdb():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    role = request.form['role_select']
    if User.query.filter_by(username=username).first():
        
        return "User already exists!" 
    else:
        max_id = db.session.query(db.func.max(User.id)).scalar() or 0
        new_id = max_id + 1
        usr = User(id=new_id, username=username, password=password, role=role, fullname=fullname)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('login'))

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
