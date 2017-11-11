from os.path import join,dirname, realpath

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_basicauth import BasicAuth
from config import classifier


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images/')

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
basic_auth = BasicAuth(app)



#import matplotlib.pyplot as plt
# Data Prepocessing 
import numpy as np
import pandas as pd


# importing the dataset
dataset = pd.read_csv('heart_processed.csv')
X = dataset.iloc[:, 0:13].values
y = dataset.iloc[:, 13].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)



from heart import views 
