import os
import rawgpy
from flask import Flask, request, render_template,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
rawg = rawgpy.RAWG("User-Agent, this should identify your app")
from random import seed
from random import random
seed(1)
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
    data_1="abcdefghijklmnopqrstuvwxy"
    return render_template("1.html",data_1=data_1)


@app.route("/search", methods=["GET"])
def search():
   return render_template("search.html")

@app.route("/result", methods=["POST"])
def results():
    search=request.form.get("anime")
    search_result = jikan.search('anime', search)
    data_anime=[]
    for i in range(0,20):
        a=search_result["results"][i]["title"]
        b=search_result["results"][i]["image_url"]
        c=search_result["results"][i]["synopsis"]
        d=search_result["results"][i]["url"]
        e=search_result["results"][i]["score"]
        f=[a,b,c,d,e]
        data_anime.append(f)

    
    return render_template("result.html",data_anime=data_anime)
@app.route("/search2", methods=["GET"])
def search2():
   return render_template("search2.html")

@app.route("/result2", methods=["POST"])
def results2():
    url = "https://rawg-video-games-database.p.rapidapi.com/games/apex"
    headers = {
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
    'x-rapidapi-key': "a9935374bemshb0147f63949e0e1p17c9d1jsn6a305965d763"
    }
    
    search=request.form.get("anime")
    response = requests.request("GET", url, headers=headers)
    h=response.json()
    
    
    data_anime=[]
    """for i in range(0,20):
        a=search_result["results"][i]["title"]
        b=search_result["results"][i]["image_url"]
        c=search_result["results"][i]["synopsis"]
        d=search_result["results"][i]["url"]
        e=search_result["results"][i]["score"]
        f=[a,b,c,d,e]
        data_anime.append(f)"""

   

    return h
       








    















@app.route("/check", methods=["POST","GET" ])
def op():
    
    
    data_3=["1","2","4","8","36","10","16","37","14","7","40","22","24"]
    data_2=["Action","Adventure","Comedy","Drama","Slice of Life","Fantasy","Magic","Supernatural","Horror","Mystery","Psychological","Romance","Sci-Fi"]
    data_1="abcdefghijklm"
    return render_template("name.html",data_1=data_1,data_2=data_2,data_3=data_3)
               
    


@app.route("/trending", methods=["POST", "GET","HEAD","PUT"])
def trending():
    
    
    

    #res = requests.get("https://kitsu.io/api/edge/users?sort=-rating" )
   # if res.status_code != 200:
    #    raise Exception("ERROR: API request unsuccessful.")
    data = jikan.top(type='anime')
    data_1=[]
    for i in range (0,25) :
        rate_1=data["top"][i]["title"]
        e=data["top"][i]["url"]
        img_src=data["top"][i]["image_url"]
        l=[rate_1, img_src,e]
        data_1.append(l)
    
    return render_template("trend.html",data_1=data_1)
    
@app.route("/ko",methods=["GET"])
def indexy():
    data=[]
    i=0
    while i<10 :
        value=random()
        value=value*10000
        value=round(value)
        try:
            mushishi = jikan.anime(value)
        except :
            continue
            
        
        a=mushishi["title"]
        b=mushishi["image_url"]
        c=mushishi["synopsis"]
        d=mushishi["url"]
        e=mushishi["genres"][0]["name"]
        if e=="Hentai":
            continue
        f=mushishi["score"]
        i=i+1
        kor=[a,b,c,d,e,f]
        data.append(kor)
    
    
    return render_template("random.html",data=data,type="anime")
    """mushishi = jikan.anime(600)
    return mushishi"""

@app.route("/kor",methods=["GET"])
def indexyy():
    data=[]
    i=0
    while i<10 :
        value=random()
        value=value*20000
        value=round(value)
        try:
            mushishi = jikan.manga(value)
        except :
            continue
            
        
        a=mushishi["title"]
        b=mushishi["image_url"]
        c=mushishi["synopsis"]
        d=mushishi["url"]
        e=mushishi["genres"][0]["name"]
        if e=="Hentai" or e=="Yaoi":
            continue
        f=mushishi["score"]
        i=i+1
        kor=[a,b,c,d,e,f]
        data.append(kor)
    
    
    return render_template("random.html",data=data,type="manga")
    """mushishi = jikan.anime(600)
    return mushishi"""








if __name__ == '__main__':
    app.run(debug=True)
