#!flask/bin/python

from flask import Flask, jsonify, abort,  make_response,  request, current_app,  g
import os
from db import get_db

import smtplib   
from email.mime.text import MIMEText   

from apscheduler.schedulers.background import BackgroundScheduler

import requests
import alpha_vantage
import json


API_URL = "https://www.alphavantage.co/query" 
alphavantageAPIkey='' # YOUR alphavantage API key ####################################

mymail = '' # YOUR MAIL.RU E-MAIL ####################################
password ='' # YOUR PASSWORD ####################################
smtp_server = 'smtp.mail.ru'


app = Flask(__name__)


app.config.from_mapping(

        SECRET_KEY='dev',

        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )


def send_email(to,text):

    msg = MIMEText('Changes in your tickers:\n'+text)
    msg['Subject'] = 'Yor tickers'
    msg['From'] = mymail
    msg['To'] = to

    s = smtplib.SMTP_SSL(smtp_server)
    s.ehlo()
    s.login(mymail, password)
    s.sendmail(mymail, [to], msg.as_string())
    s.quit()



def mailing():
    with app.app_context():
        db = get_db()
        allsub = db.execute(
            'SELECT *'
            ' FROM subscriptions'
        ).fetchall()
    

    for sub in allsub:
        mail=sub[0]
        symbol=sub[1]
        max_val=sub[2]
        min_val=sub[3]
        data = { "function": "TIME_SERIES_INTRADAY", 
        "symbol": symbol,
        "interval" : "60min",       
        "datatype": "json", 
        "apikey": "WG0S797AUXLLSIW9" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        #print(symbol)
        a = (data['Time Series (60min)'])
        #print (a)
        keys = (a.keys())
        for key in keys:
            high=a[key]['2. high']
            low=a[key]['3. low']
            break
        if max_val!="" and float(high)>float(max_val):
            send_email(mail,"Your ticker "+symbol+"is above the threshold("+max_val+"): "+high)
        if min_val!="" and float(low)<float(min_val):
            send_email(mail,"Your ticker "+symbol+"is below the threshold("+min_val+"): "+low)





scheduler = BackgroundScheduler()
scheduler.add_job(func=mailing, trigger='interval', seconds=3600)
scheduler.start()






# POST /subscription Content-Type: application/json { "ticker": "TSLA", "email": "mail@example.com" "max_price": "270.5200", "min_price": "240.200", }
# curl -i -H "Content-Type: application/json" -X POST -d "{ """ticker""": """PINS""", """email""": """dark.android7@gmail.com""", """max_price""": """25.14""", """min_price""": """25.14""" }" http://localhost:5000/subscription
@app.route('/subscription', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    else:    
        
        error = None

        try:
            email = request.json['email']
        except KeyError:
            error = 'Email is required.'

        try:
            ticker = request.json['ticker']
        except KeyError:
            error = 'Ticker is required.'

        try:
            max_price = request.json['max_price']
        except KeyError:
            max_price = None
 
        try:
            min_price = request.json['min_price']
        except KeyError:
            min_price = None

            
        if max_price is None and min_price is None:
            error = 'Max or Min is required.'

        if error is not None:
            abort(404, error)
        else:

            db = get_db()
            state = db.execute(
                'SELECT *'
                ' FROM subscriptions'
                ' WHERE email=\''+email+'\''
            ).fetchall()  

            if len(state)<=5:


                db = get_db()
                db.execute(
                    'INSERT INTO subscriptions (email, ticker, max_price, min_price)'
                    ' VALUES (?, ?, ?, ?)',
                    (email, ticker, max_price, min_price)
                )
                db.commit()
                return "Added"

            else:
                abort(404, "You have reached your limit")

    return "not added, try again"


# DELETE /subscription?email=mail@example.com&ticker=TSLA  
# curl -i -H "Content-Type: application/json" -X DELETE -d "{ """ticker""": """TSLA""", """email""": """mail@example.com"""}" http://localhost:5000/unsubscription
@app.route('/unsubscription', methods=['DELETE'])
def delete():
    
    if not request.json:
        abort(400)
    else:    

        error = None


        try:
            email = request.json['email']
        except KeyError:
            error = 'Email is required.'

        try:
            ticker = request.json['ticker']
        except KeyError:
            ticker = None




        if error is not None:
            abort(404, error)
        elif ticker is not None:   
  
            db = get_db()
            db.execute(
                'DELETE FROM subscriptions'
                ' WHERE email=\''+email+'\' and ticker=\''+ticker+'\''
            )
            db.commit()
            return "Deleted by ticker"
        
        else:
            
            db = get_db()
            db.execute(
                'DELETE FROM subscriptions'
                ' WHERE email=\''+email+'\''
            )
            db.commit()
            return "Deleted all"      






    return "not deleted, try again"








if __name__ == '__main__':
    app.run(debug=True)
    

