from flask import Flask, redirect, render_template, url_for, request,flash
import requests
from .models import Token
import json
import jwt as JWT

app = Flask (__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/',methods=['POST'])
def index_post():  
   
    if 'createmeeting' in request.form : 
        url="http://192.168.2.243:5000/vcapi/v1/createmeeting"
        roomname=request.form.get('roomname') 
        owner=request.form.get('owner') 
        print(roomname,' ',owner)
        appsecret = app.config['SECRET_KEY']
        token =  Token()
        jwt = token.generateToken_CreateMeeting(roomname,owner,appsecret) 
        r= requests.post(url,json.dumps(jwt))
        #print(r.status_code, r.reason,r.text)
        print("Result Test = ",r.text)
        retVal = token.decodeToken(r.text,appsecret)
        if 'error' in retVal:
            flash("Result: Invalid JWT Token" )
        else :
            flash("Result: "+retVal['result']+', Password: '+retVal['password'] )
        return render_template('index.html')
    elif 'startmeeting' in request.form : 
        url="http://192.168.2.243:5000/vcapi/v1/startmeeting"
        roomname=request.form.get('roomname') 
        name=request.form.get('owner') 
        password =request.form.get('password') 
        moderator=request.form.get('moderator') 
        print(roomname,' ',name,' ',password,' ',moderator)
        appsecret = app.config['SECRET_KEY']
        token =  Token()
        jwt = token.generateToken_StartMeeting(roomname,name,password,moderator,appsecret)
        #print(jwt)
        r = requests.post(url,json.dumps(jwt))
        #print(r.status_code, r.reason,r.text)
        #retVal = token.decodeToken(r.text,appsecret)
        rslt = r.text#retVal['result']
        print(rslt)
        if "error" in rslt:
            flash("Result: "+rslt)
            return render_template('index.html')
        else:  
            return (r.text)
    
