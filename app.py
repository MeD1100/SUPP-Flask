# -*- coding: utf-8 -*-
from asyncore import read
from threading import Timer
import webbrowser
from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource, abort
from script_scrap_post import Scrap_post
#from configuration_file import 
from insert_posts_mongoDB import insert_comment, insert_post

# from excel_manipulation import read_excel_lines

from flask_cors import CORS, cross_origin
import pymongo
import json

from common import cache


app = Flask(__name__)

cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

CORS(app)

datas=[]
app.config['JSON_AS_ASCII'] = False
api = Api(app)
nb_scroll_react = 5
nb_scroll_share = 5
nb_click = 5

# list_urls=["https://www.facebook.com/algerianreds/posts/6107700535936870"] #text


weather = {
     "data": [
     {
         "day": "1/6/2019",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2016",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2018",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2017",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2015",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2014",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     {
         "day": "1/6/2013",
         "temperature": "23",
         "windspeed": "16",
         "event": "Sunny"
     },
     ]
    }


@app.route("/", methods=['GET'])
def index():
    return "Welcome to CodezUp"

@app.route("/weatherReport",methods=["GET"])
def WeatherReport():
     global weather
     return jsonify([weather])

@app.route("/api/saveUrl",methods = ["POST","GET"])
def saveUrl():
     if request.method == "POST":
        # print(request.form, flush=True)

        url = request.json["url"]
        print(url)

        # url = request.form.get("url")
        
        connection = pymongo.MongoClient("mongodb+srv://mohamed:21328166@cluster0.ifzz03r.mongodb.net/?retryWrites=true&w=majority")
        database = connection['Sauvegarde_urls']
        url_db=database['urls']

        url_db.insert_one({'status':'OK','url':url})
        cache.delete(url)
        cache.set("list_urls", url)
        
        Timer(1, open_browser).start()
        
        return jsonify(data = "The url was successfully added.")
     if request.method == "GET":
        
        url = cache.get("list_urls")

        return jsonify({'url':url})

from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))

# exemple = [
#     {
#         "who_share": [
#             "نك أم أمك يا نور القحبة DZ",
#             "ليفربول DZ",
#             "ليفربول DZ",
#             "Samo Yousef"
#         ],
#         "_id": {
#             "$oid": "62f436f196d2534078654167"
#         }
#     }
# ]

# exemple2 = "\u0644\u064a\u0641\u0631\u0628\u0648\u0644"
import json
from bson.objectid import ObjectId

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj


import json
import os

def where_json(file_name):
    return os.path.exists(file_name)


class scrapy_facebook(Resource):
    def get(self):
        
        if where_json('json_data.json'):
            with open('json_data.json', 'r', encoding='utf-8') as f:
                table = json.loads(f.read())
            return jsonify([table])
    
        else:
            url_post = cache.get("list_urls")
            # print("saret hedhi?")
            data=Scrap_post(url_post,nb_scroll_react,nb_scroll_share)
            insert_post(data)
            datas.append(data)

            with open('json_data.json', 'w', encoding='utf-8') as outfile:
                json.dump(datas[0], outfile, cls=Encoder, ensure_ascii=False)

            Timer(1, open_browser).start()
            
            # return json.dumps(exemple2, ensure_ascii=False).encode('utf8').decode()   

api.add_resource(scrapy_facebook, '/api/scrapingPostFacebook')


@app.route('/api/scrapedData',methods=['GET'])
def send_scrapedData():
    if where_json('json_data.json'):
        with open('json_data.json', 'r', encoding='utf-8') as f:
            table = json.loads(f.read())
        return jsonify([table])
    return jsonify(datas="no json file is found yet..")

@app.route('/api/predictResults', methods=['GET','POST'])
def send_prediction():
    return jsonify({"result":'90%'})
    

    

# def open_scrapedData_route():
#     webbrowser.open_new('http://127.0.0.1:5000/api/scrapedData')
def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/api/scrapingPostFacebook')



if __name__ == '__main__':
    app.run(debug=True)