from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS

from db_control import crud, mymodels

import requests

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://tech0-gen-8-step3-app-node-8.azurewebsites.net"
        ],
        "support_credentials": True
    }
})


@app.route("/")
def index():
    result = crud.myselect2()
    return "<p>Flask top page!</p>"

@app.route("/register/user", methods=['POST'])
def create_register_user():
    values = request.get_json()
    print(values)
    tmp = crud.myinsert2(values)
    return True

@app.route("/customers", methods=['POST'])
def create_customer():
    values = request.get_json()
    # values = {
    #     "customer_id": "C005",
    #     "customer_name": "佐藤Aこ",
    #     "age": 64,
    #     "gender": "女"
    # }
    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['GET'])
def read_one_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.myselect(mymodels.Customers, target_id)
    return result, 200

@app.route("/allcustomers", methods=['GET'])
def read_all_customer():
    model = mymodels.Customers
    result = crud.myselectAll(mymodels.Customers)
    return result, 200

@app.route("/customers", methods=['PUT'])
def update_customer():
    print("I'm in")
    values = request.get_json()
    values_original = values.copy()
    model = mymodels.Customers
    # values = {  "customer_id": "C004",
    #             "customer_name": "鈴木C子",
    #             "age": 44,
    #             "gender": "男"}
    tmp = crud.myupdate(model, values)
    result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['DELETE'])
def delete_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.mydelete(model, target_id)
    return result, 200

@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200


@app.route("/recommend/user", methods=['POST'])
def recommend_customer():
    values = request.get_json()
    result = crud.recommendselect(values)
    return json.dumps(result), 200
    # return response.json(), 200


@app.route("/companies", methods=['GET'])
def read_all_companies():
    result = crud.myselect2()
    return json.dumps(result), 200

