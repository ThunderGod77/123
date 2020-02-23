import os

from flask import Flask, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests


import json
from jikanpy import Jikan
jikan = Jikan()



app = Flask(__name__)



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("1.html")









@app.route("/new", methods=["POST","GET"])
def new():
   return render_template("register.html",error="")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)














@app.route("/login", methods=["POST","GET"])
def login():
    return render_template("log.html")

@app.route("/check", methods=["POST", ])
def op():
    name=request.form.get("name")
    
    password = request.form.get("password")
    persons = db.execute("SELECT* FROM users ").fetchall()
    
    
    if persons is None :
        
        return render_template("ui.html") 
    else :
        
        for person in persons :
            
            if name == person.name and password == person.password :
                data = db.execute("SELECT * FROM all_data WHERE user_id = :id", {"id": person.id}).fetchall()
                
                return render_template("name.html",name=name,data=data)
               
    return render_template("ui.html") 


@app.route("/trending", methods=["POST", "GET","HEAD","PUT"])
def trending():
    
    
    res = requests.get("https://api.rawg.io/api/games?dates=2019-01-01,2019-12-31&ordering=-added")
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    data_2=[]
    for i in range (0,20) :
        rate_1=data["results"][i]["name"]
        e=data["results"][i]["clip"]["clips"]["640"]
        img_src=data["results"][i]["clip"]["preview"]
        l=[rate_1, img_src,e]
        data_2.append(l)
    

    #res = requests.get("https://kitsu.io/api/edge/users?sort=-rating" )
   # if res.status_code != 200:
    #    raise Exception("ERROR: API request unsuccessful.")
    data = jikan.top(type='anime')
    data_1=[]
    for i in range (0,22) :
        rate_1=data["top"][i]["title"]
        e=data["top"][i]["url"]
        img_src=data["top"][i]["image_url"]
        l=[rate_1, img_src,e]
        data_1.append(l)
    
    return render_template("trend.html",data_1=data_1,data_2=data_2)
    











if __name__ == '__main__':
    app.run(debug=True)
