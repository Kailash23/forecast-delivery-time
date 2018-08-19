# standard py libs
import os

# project dependencies
from flask import Flask, request, send_from_directory, jsonify
from pprint import pprint
import googlemaps
import pymongo
from pymongo import MongoClient

# project modules
from utils import load_data, package_data, get_regressor
from regression import predict

import warnings
warnings.filterwarnings('ignore')


city_matrix, X, y, delay_times = load_data()
regressor = get_regressor(X, y)

app = Flask(__name__)

#DEFAULT
@app.route('/')
def index():
    return send_from_directory('public','index.html')

#HTML ROUTES
@app.route('/index.html')
def index2():
    return send_from_directory('public','index.html')

@app.route('/login.html')
def index3():
    return send_from_directory('public','login.html')

@app.route('/home.html')
def index4():
    return send_from_directory('public','home.html')

@app.route('/order.html')
def index5():
    return send_from_directory('public','order.html')

@app.route('/rollover.html')
def index6():
    return send_from_directory('public','rollover.html')

#JS ROUTES
@app.route('/scripts/app.js')
def index_app_script():
    return send_from_directory('public/scripts', 'app.js')

@app.route('/scripts/rollover.js')
def index_app_script1():
    return send_from_directory('public/scripts', 'rollover.js')

#CSS ROUTES
@app.route('/styles/form.css')
def index_styles():
    return send_from_directory('public/styles', 'form.css')

@app.route('/styles/home.css')
def index_styles1():
    return send_from_directory('public/styles', 'home.css')

@app.route('/styles/rollover.css')
def index_styles2():
    return send_from_directory('public/styles', 'rollover.css')

@app.route('/styles/signin.css')
def index_styles3():
    return send_from_directory('public/styles', 'signin.css')

# ASSETS
@app.route('/assets/cpu.jpg')
def index_assets():
    return send_from_directory('public/assets', 'cpu.jpg')

@app.route('/assets/flip.jpg')
def index_assets1():
    return send_from_directory('public/assets', 'flip.jpg')

@app.route('/assets/keyboard.jpg')
def index_assets2():
    return send_from_directory('public/assets', 'keyboard.jpg')

@app.route('/assets/laptop.jpg')
def index_assets3():
    return send_from_directory('public/assets', 'laptop.jpg')

@app.route('/assets/monitor.jpg')
def index_assets4():
    return send_from_directory('public/assets', 'monitor.jpg')

@app.route('/assets/mouse.jpg')
def index_assets5():
    return send_from_directory('public/assets', 'mouse.jpg')

#SVG
@app.route('/assets/delivery.svg')
def index_assets6():
    return send_from_directory('public/assets', 'delivery.svg')

@app.route('/assets/dell.svg')
def index_assets7():
    return send_from_directory('public/assets', 'dell.svg')

@app.route('/assets/truck.svg')
def index_assets8():
    return send_from_directory('public/assets', 'truck.svg')

@app.route('/assets/whitedell.svg')
def index_assets9():
    return send_from_directory('public/assets', 'whitedell.svg')

gmaps1 = googlemaps.Client(key='AIzaSyC4dICfe5c823PPYcjeCefHV7C6uxsntpQ')

def call_dist_matrix_api(shipping_city, delivery_city):
    response = gmaps1.distance_matrix(shipping_city, delivery_city)
    print(response)
    response = response['rows'][0]['elements'][0]
    if response['status'] == 'NOT_FOUND':
        print('Unknown Location!')
        return None
    dist_kms = response['distance']['value'] / 1000
    time_hrs = response['duration']['value'] / 3600
    city_matrix[shipping_city][delivery_city] = [dist_kms, time_hrs]
    return dist_kms

def calc_shortest_path(city='Pune'):
    min_dist = 10000
    closest_shipping_center = 'Delhi'

    for key, cities in city_matrix.items():
        if cities.get(city, -0.234) != -0.234:
            dist = cities[city][0]
        else:
            dist = call_dist_matrix_api(key, city)
            if dist == None:
                return None
        if dist < min_dist:
            min_dist = dist
            closest_shipping_center = key
    return closest_shipping_center

@app.route('/get-delivery-estimate/')
def getDeliveryEstimate():
    weather = 0
    transport_mode = 0

    delivery_city = request.args.get('city')
    shipping_city = calc_shortest_path(delivery_city)

    if shipping_city == None:
        return jsonify({'result': 'Unknown City', 'status': 'failed'})

    delay_time = delay_times[shipping_city]
    print('{} -> {}'.format(shipping_city, delivery_city))
    dist = city_matrix[shipping_city][delivery_city][0]

    X = [weather, transport_mode, delay_time, dist]

    prediction = '{:.2f}'.format(predict(regressor, [X])[0])
    print('Prediction: {}'.format(prediction))

    return package_data(prediction, db.users.find_one({'email': 'test@gmail.com'}))
    

if __name__ == '__main__':
    # MONGO CONNECTION
    client = MongoClient('mongodb://kailash23:kailash23@ds125482.mlab.com:25482/dell-project-mongo-db')
    # DATABASE CONNECTION
    global db
    db = client['dell-project-mongo-db']
    # # TABLE/COLLECTION CURSOR
    # users_collection = db.users
    
    # # OBJECT INSERTION - returns Inserted Object's ID
    # object_id = users_collection.insert_one({"email": "test@gmail.com", "password": "testpwd"}).inserted_id
    
    # # QUERY/FIND A DOCUMENT IN COLLECTION USING ID
    # test_user = users_collection.find_one({"_id": object_id})
    # pprint(test_user)
    # pskrunner14 = users_collection.find_one({"email": "pskrunner14@gmail.com"})
    # pprint(pskrunner14)

    # # RETRIEVE ALL DOCUMENTS
    # for user in users_collection.find():
    #     pprint(user)

    app.run(debug=True)