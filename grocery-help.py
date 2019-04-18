from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request, jsonify
from flask import make_response
from flaskext.mysql import MySQL
from flask import render_template, json
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'db1'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

def Authenticate(entity):
    sub = entity
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT Marks from marks where Subjects='" + sub + "'")
    data = cursor.fetchone()
    if data is None:
        return "No such subject"
    else:
        speech="Marks in subject:" + str(data)
        return speech

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

def results():
    # build a request object
    req = request.get_json(silent=True,force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    return { "fulfillmentText": res }

def processRequest(req):
    action = req['queryResult']['action']
    if req['queryResult']['action'] != "marks":
        return {}
    entity=req['queryResult']['parameters']['Subjects']
    res = Authenticate(entity)
    #print(res)
    return res
##def makeWebhookResult(data):
##    print ("starting makeWebhookResult...")
##
##    #s=cursor.fetchone()cur.execute("SELECT * FROM marks Where Subjects = %s", [data])
##    #speech="Marks in subject:" + data
##
##
##    print("Response:")
    #print(speech)
##    return {'fulfillmentText':'Marks in subject:' + data
##    
##        #"speech": speech,
##        #"displayText": speech,
##        # "data": "data",
##        #"contextOut": [],
##        #"source": "apiai-weather-webhook-sample"
##        #"source":"localhost"
##        }


if __name__ == '__main__':
    app.run()





    
