from flask import Flask, jsonify, request
from redis import Redis, ConnectionPool
import time
import json

POOL = ConnectionPool(host='ec2-18-188-68-114.us-east-2.compute.amazonaws.com', decode_responses=True, port=6379, db=0)
redis = Redis(connection_pool=POOL)

app = Flask(__name__)

def create_api_key(api_name,api_scope,limit,per):
    key =  api_name+":"+api_scope
    val_dict = {"limit":limit,"per":per}
    val_json = json.dumps(val_dict)
    redis.set(key, val_json)
    return key


@app.route('/')
def index():
    return "Index Page"


@app.route('/register', methods=['POST'])
def register_api():
    input_json = request.json
    api_name = input_json['api_name']
    api_scope = input_json['api_scope'] 
    limit = input_json['limit']
    per = input_json['per']
    api_key = create_api_key(api_name,api_scope,limit,per)
    return jsonify({"api_key":api_key})


@app.route('/unregister', methods=['POST'])
def unregister_api():
    if 'api_key' in request.get_json():
        api_key = request.get_json()['api_key']
    
    if api_key is not None:
        redis.delete(api_key)
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"failure"})


@app.route('/process', methods=['POST'])
def process_api():
    request_json = request.json
    api_key = request_json['api_key']
    api_data = redis.get(api_key)
    api_data_json = json.loads(api_data)
    limit = int(api_data_json['limit'])
    per = int(api_data_json['per'])
    counter_key = api_key + ":counter"
    
    now = int(time.time()*1000)
    old = now - (per*1000)
    redis.zremrangebyscore(counter_key,0,old)
    
    if redis.zcard(counter_key) < limit:
        redis.zadd(counter_key, now, now)
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"failure"}) 
    

if __name__ == '__main__':
    app.run(debug=True)
