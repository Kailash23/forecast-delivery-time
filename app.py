# standard py libs
import os

# project dependencies
from flask import Flask, request, send_from_directory

# project modules
from utils import load_data, package_data, get_regressor
from regression import predict

import warnings
warnings.filterwarnings('ignore')

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

def calc_shortest_path(city='Pune'):
    min_dist = 10000
    closest_shipping_center = 'Delhi'
    for key, cities in city_matrix.items():
        if float(cities[city][0]) < min_dist:
            min_dist = cities[city][0]
            closest_shipping_center = key
    return closest_shipping_center

@app.route('/get-delivery-estimate/')
def getDeliveryEstimate():
    weather = 1
    transport_mode = 0
     #delay_time = 48  #we will store average waiting time of each centers

    delivery_city = request.args.get('city')
    shipping_city = calc_shortest_path(delivery_city)

    delay_time = delay_times[shipping_city]

    print('{} -> {}'.format(shipping_city, delivery_city))

    dist = city_matrix[shipping_city][delivery_city][0]

    X = [weather, transport_mode, delay_time, dist]

    prediction = '{:.2f}'.format(predict(regressor, [X])[0])
    print('Prediction: {}'.format(prediction))

    return package_data(prediction)
    

if __name__ == '__main__':
    app.run(debug=True)