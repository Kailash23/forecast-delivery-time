import os

from flask import jsonify
import pickle
import pandas as pd
import math

from generator import make_city_matrix, make_dataset, delay_time_dictionary
from regression import train

import warnings
warnings.filterwarnings('ignore')

def get_regressor(X, y):
    if os.path.isfile('data/linear_regressor.pkl'):
        with open('data/linear_regressor.pkl', 'rb') as file:
            regressor = pickle.load(file)
    else:
        X_train, X_test, y_train, y_test = X[: -1000], X[-1000: ], y[: -1000], y[-1000: ]
        regressor, r2_score, rmse = train(X_train, y_train, X_test, y_test)
        with open('data/linear_regressor.pkl', 'wb') as file:
            pickle.dump(regressor, file)
        print('Finished training regressor')
        print('R2 Score: {}'.format(r2_score))
        print('RMSE: {}'.format(rmse))
    return regressor

def load_data():
    if os.path.isfile('data/city_matrix.pkl'):
        with open('data/city_matrix.pkl', 'rb') as file:
            city_matrix = pickle.load(file)
    else:
        city_matrix = make_city_matrix()
        with open('data/city_matrix.pkl', 'wb') as file:
            pickle.dump(city_matrix, file)
    
    if os.path.isfile('data/dataset.pkl'):
        with open('data/dataset.pkl', 'rb') as file:
            X, y = pickle.load(file)
    else:
        X, y = make_dataset(8000, city_matrix)
        with open('data/dataset.pkl', 'wb') as file:
            pickle.dump((X, y), file)

    return city_matrix, X, y, delay_time_dictionary

def package_data(prediction):
    data = {'result': prediction, 'status': 'success' }
    return jsonify(data)