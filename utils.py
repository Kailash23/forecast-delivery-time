import os

from flask import jsonify
import pickle
import json
import pandas as pd

from generator import make_city_matrix, make_dataset
from regression import train

import warnings
warnings.filterwarnings('ignore')

def get_regressor(X, y):
    if os.path.isfile('data/linear_regressor.pkl'):
        with open('data/linear_regressor.pkl', 'rb') as file:
            regressor = pickle.load(file)
    else:
        X_train, X_test, y_train, y_test = X[: -1500], X[-1500: ], y[: -1500], y[-1500: ]
        regressor, r2_score, rmse = train(X_train, y_train, X_test, y_test)
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
    
    if os.path.isfile('data/dataset.pkl'):
        with open('data/dataset.pkl', 'rb') as file:
            X, y = pickle.load(file)
    else:
        X, y = make_dataset(4000, city_matrix)

    return city_matrix, X, y

def package_data(prediction):
    data = {'prediction': prediction}
    data = json.dumps(data)
    return jsonify(data)