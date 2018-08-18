# standard py libs
import os
from math import ceil
import requests,json
# project dependencies
from flask import Flask, request, send_from_directory, jsonify
from find_weather import find_weather
from math import randint

# project modules
from utils import load_data, package_data, get_regressor
from regression import predict

import warnings
warnings.filterwarnings('ignore')

import googlemaps

city_matrix, X, y, delay_times = load_data()
regressor = get_regressor(X, y)

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('public','index.html')
@app.route('/index.html')
def index2():
    return send_from_directory('public','index.html')
@app.route('/scripts/app.js')
def index_app_script():
    return send_from_directory('public/scripts', 'app.js')
@app.route('/styles/main.css')
def index_styles():
    return send_from_directory('public/styles', 'main.css')

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
            min_dist = cities[city][0]
            closest_shipping_center = key
    return closest_shipping_center

@app.route('/get-delivery-estimate/')
def getDeliveryEstimate():
    
    transport_mode = 0

    delivery_city = request.args.get('city')
    shipping_city = calc_shortest_path(delivery_city)

    if shipping_city == None:
        return jsonify({'result': 'Unknown City', 'status': 'failed'})

    delay_time = delay_times[shipping_city]
    weather_type = find_weather(shipping_city)
    source_weather = weather_type[ceil(delay_time/24)].lower() 
    
    if 'storm' in source_weather:
        weather = 2
    if 'rain' in source_weather:
        weather = 1
    print('{} -> {}'.format(shipping_city, delivery_city))
    dist = city_matrix[shipping_city][delivery_city][0]

    X = [weather, transport_mode, delay_time, dist]

    prediction = '{:.2f}'.format(predict(regressor, [X])[0])
    print('Prediction: {}'.format(prediction))

    if 'storm' in 

    return package_data(prediction)
    

if __name__ == '__main__':
    app.run(debug=True)
