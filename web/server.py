from flask import Flask, request, send_from_directory, render_template
import json
from os import listdir
from parser import xml_parser as xs
from redis_helper import getdata
# set the project root directory as the static folder, you can set others.
# app = Flask(__name__, static_url_path='/home/user/nlproject/web')
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    print("aayame")
    name="apoorva"
    return render_template('index.html', name=name)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/get/files')
def get_files():
    lang = request.args.get('lang')
    tag =  request.args.get('tag')
    #tag means test, train and annotated.
    if tag=="all" and lang=="en":
        all=listdir('/home/user/nlproject/data/English/Test')
        all=all+listdir('/home/user/nlproject/data/English/Train')
        all=all+listdir('/home/user/nlproject/data/English/unannotated')
    ret_str=json.dumps(all)
    return ret_str

def text(ret):
    qw=""
    for x in ret:
        qw=qw+" "+x[1]
    return qw

def getargs(ret):
    l = ['TIME-ARG','PLACE-ARG','CASUALTIES-ARG','REASON-ARG','PARTICIPANT-ARG']
    ls={'TIME-ARG':[],'PLACE-ARG':[],'CASUALTIES-ARG':[],'REASON-ARG':[],'PARTICIPANT-ARG':[]}
    for x in ret:
        key=x[0]
        value=x[1]
        if(l[0] in key):
            ls[l[0]].append(value)
        elif(l[1] in key):
            ls[l[1]].append(value)
        elif(l[2] in key):
            ls[l[2]].append(value)
        elif(l[3] in key):
            ls[l[3]].append(value)
        elif(l[4] in key):
            ls[l[4]].append(value)
    return ls

def helper(add,filename):
    doc,a,b=xs(add)
    ret=doc[filename]
    event_name=a[filename]
    content=text(ret)
    args1=getargs(ret)
    jsonx={"event_type":event_name,"content":content,"args":args1}
    return jsonx

@app.route('/get/data')
def get_data():
    filename = request.args.get('filename')
    #import pdb;pdb.set_trace()
    all=listdir('/home/user/nlproject/data/English/Test')
    if(filename in all):
        jsonx=helper('/home/user/nlproject/data/English/Test/',filename)
        model_data=getdata(filename,jsonx["content"])
        jsonx["model_data"]=model_data
        return json.dumps(jsonx)
    all=listdir('/home/user/nlproject/data/English/Train')
    if(filename in all):
        jsonx=helper('/home/user/nlproject/data/English/Train/',filename)
        model_data=getdata(filename,jsonx["content"])
        jsonx["model_data"]=model_data
        return json.dumps(jsonx)
    all=listdir('/home/user/nlproject/data/English/unannotated')
    if(filename in all):
        jsonx=helper('/home/user/nlproject/data/English/unannotated/',filename)
        model_data=getdata(filename,jsonx["content"])
        jsonx["model_data"]=model_data
        return json.dumps(jsonx)

if __name__ == '__main__':
    app.run(debug=True)
