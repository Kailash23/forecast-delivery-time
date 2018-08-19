from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

import warnings
warnings.filterwarnings('ignore')   #avoiding warning

def train(X_train, y_train, X_test, y_test):
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    r2_score = regressor.score(X_test, y_test)
    prediction = regressor.predict(X_test)
    rmse = mean_squared_error(y_test, prediction)
    return regressor, r2_score, rmse

def predict(regressor, X_predict):
    return regressor.predict(X_predict)