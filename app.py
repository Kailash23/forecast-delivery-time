# standard py libs
import os

# project dependencies
from flask import Flask, request, send_from_directory, jsonify, redirect, session, render_template
from pprint import pprint
import googlemaps
import pymongo
from pymongo import MongoClient

# project modules
from utils import load_data, package_data, get_regressor
from regression import predict

import warnings
warnings.filterwarnings('ignore')


city_matrix, X, y, delay_time_dictionary = load_data()
regressor = get_regressor(X, y)

app = Flask(__name__)
app.secret_key = 'kailash_uniyal_04'

#DEFAULT
@app.route('/')
def index():
    return send_from_directory('public','index.html')

#HTML ROUTES
@app.route('/<path:path>')
def index2(path):
    return send_from_directory('public', path)

#JS ROUTES
@app.route('/scripts/<path:path>')
def index_app_script(path):
    return send_from_directory('public/scripts', path)

#CSS ROUTES
@app.route('/styles/<path:path>')
def index_styles(path):
    return send_from_directory('public/styles', path)

# ASSETS
@app.route('/assets/<path:path>')
def index_assets(path):
    return send_from_directory('public/assets', path)

gmaps1 = googlemaps.Client(key='AIzaSyC4dICfe5c823PPYcjeCefHV7C6uxsntpQ')

# FUNCTION CALCULATING SHORTEST DISTANCE FROM SHIPPING CENTER TO DELIVERY CENTER
def call_dist_matrix_api(shipping_city, delivery_city):
    response = gmaps1.distance_matrix(shipping_city, delivery_city)
    response = response['rows'][0]['elements'][0]

    if response['status'] == 'NOT_FOUND':
        print('Unknown Location!')
        return None

    dist_kms = response['distance']['value'] / 1000
    time_hrs = response['duration']['value'] / 3600
    city_matrix[shipping_city][delivery_city] = [dist_kms, time_hrs]    # if city - not found in matrix then save it
    return dist_kms

def calc_shortest_path(city='Pune'):
    min_dist = 10000
    closest_shipping_center = 'Delhi'

    for key, cities in city_matrix.items():
        if cities.get(city, -0.234) != -0.234:       # if city is not stored in the matrix call Distance Matrix Api
            dist = cities[city][0]
        else:
            dist = call_dist_matrix_api(key, city)
            if dist == None:
                return None
        if dist < min_dist:
            min_dist = dist
            closest_shipping_center = key
    return closest_shipping_center

@app.route('/get-products')
def products():
    products_collection = db.products
    products = []
    for product in products_collection.find():
        products.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'thumb': product['thumb']})
    #print(products)
    return jsonify(products)

@app.route('/get-orders')
def orders():
    products_collection = db.products
    products = []
    for product in products_collection.find():
        products.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'thumb': product['thumb']})
   
    orders_collection = db.orders
    orders = []
    for order in orders_collection.find():
        orders.append({"delivery_estimate": order['delivery_estimate'], "product_id": order['product_id'], "city": order['city']})

    results = []
    for order in orders:
        for product in products:
            if order['product_id'] == product['id']:
                results.append({'address': order['city'], 'delivery_estimate': order['delivery_estimate'], 'name': product['name']})

    return jsonify(results)


@app.route('/rollover', methods=['POST', 'GET'])
def rollover():
    if request.method == 'POST':
        result = request.form
        
        city = result['city']
        product_id = result['order_id']

        orders_collection = db.orders
        orders_collection.insert_one({"order_id": "14234234123", "delivery_estimate": getDeliveryEstimate(city), "product_id": product_id, "city": city})
        return redirect("rollover.html")

@app.route('/place-order', methods=['POST', 'GET'])
def index5():
    if request.method == 'POST':
        result = request.form
        order_id = result['order_id']
        return render_template('order.html', order_id=order_id)

def getDeliveryEstimate(delivery_city):
    weather = 1     # Weather (default)
    transport_mode = 1      # transport  (default)
    product_category_number = 1     # product category   (default)
    product_delay_time = delay_time_dictionary[product_category_number]         # delay time (default)

    shipping_city = calc_shortest_path(delivery_city)       # shortest city  

    if shipping_city == None:
        return jsonify({'result': 'Unknown City', 'status': 'failed'})

    print('{} -> {}'.format(shipping_city, delivery_city))
    dist = city_matrix[shipping_city][delivery_city][0]

    X = [product_category_number, weather, transport_mode, product_delay_time, dist]

    prediction = '{:.2f}'.format(predict(regressor, [X])[0])
    # print('Prediction: {}'.format(prediction))

    return prediction
    

if __name__ == '__main__':
    # MONGO CONNECTION
    client = MongoClient('mongodb://kailash:kailash23@ds135029.mlab.com:35029/delivery-system-db')
    # DATABASE CONNECTION
    global db
    db = client['delivery-system-db']

    if os.getenv('ENV', 'dev') == 'prod':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='localhost', port=port, debug=True)
    else:
        app.run(host='localhost', debug=True)

#*************** Mongo DB Basics ***************************************************************************

# # TABLE/COLLECTION CURSOR
# users_collection = db.users


# # OBJECT INSERTION - returns Inserted Object's ID
# object_id = users_collection.insert_one({"email": "test@gmail.com", "password": "testpwd"}).inserted_id


# # QUERY/FIND A DOCUMENT IN COLLECTION USING ID
# test_user = users_collection.find_one({"_id": object_id})
# pprint(test_user)
# kailash23 = users_collection.find_one({"email": "kailash23@gmail.com"})
# pprint(kailash23)


# # RETRIEVE ALL DOCUMENTS
# for user in users_collection.find():
#     pprint(user)

#**********************************************************************************************************