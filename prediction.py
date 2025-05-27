# === Import libraries ===
import warnings
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, make_scorer
warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
#cfrom xgboost import XGBRegressor
import matplotlib.pyplot as plt
from scipy.stats import randint
import seaborn as sns
import pandas as pd
import numpy as np

car = pd.read_csv('/kaggle/input/used-car-price-prediction-dataset/used_cars.csv')

print(car.info())
print(car.shape)

# Clean 'price' and 'milage' columns
car['price'] = car['price'].str.replace('$', '').str.replace(',', '').astype(int)
car['milage'] = car['milage'].str.replace(' mi.', '').str.replace(',', '').astype(int)