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

# Custom RMSE function
def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Separate target
car_labels = car['price'].copy()
car = car.drop('price', axis=1)

# === Impute Missing Values ===
imputer_num = SimpleImputer(strategy="median")
imputer_cat = SimpleImputer(strategy="constant", fill_value="Unknown")
car_num = car.select_dtypes(include=[np.number])
car_cat = car.select_dtypes(exclude=[np.number])

car_num_tr = pd.DataFrame(imputer_num.fit_transform(car_num), columns=car_num.columns, index=car.index)
car_cat_tr = pd.DataFrame(imputer_cat.fit_transform(car_cat), columns=car_cat.columns, index=car.index)
car = pd.concat([car_num_tr, car_cat_tr], axis=1)
print("Missing values after initial imputation:")
print(car.isnull().sum())

# Reduce Dimensionality (Group Rare Categories)
for col in ['ext_col', 'int_col', 'brand', 'fuel_type', 'transmission', 'model_grouped']:
    value_counts = car[col].value_counts()
    car[col] = car[col].apply(lambda x: x if value_counts[x] >= 50 else 'Other')

# Extract horsepower and liters with improved imputation
car['horsepower'] = car['engine'].str.extract(r'(\d+\.?\d*)\s*HP').astype(float)
car['liters'] = car['engine'].str.extract(r'(\d+\.?\d*)\s*L').astype(float)
# Check for NaN values after extraction
print("NaN values in horsepower before imputation:", car['horsepower'].isnull().sum())
print("NaN values in liters before imputation:", car['liters'].isnull().sum())


# Impute horsepower and liters with median by brand, then overall median if still NaN
car['horsepower'] = car.groupby('brand')['horsepower'].transform(lambda x: x.fillna(x.median()))
car['liters'] = car.groupby('brand')['liters'].transform(lambda x: x.fillna(x.median()))
# If any NaN values remain (e.g., brands with all NaN values), fill with overall median
overall_horsepower_median = car['horsepower'].median()
overall_liters_median = car['liters'].median()
car['horsepower'] = car['horsepower'].fillna(overall_horsepower_median)
car['liters'] = car['liters'].fillna(overall_liters_median)
# Verify no NaN values remain
print("NaN values in horsepower after imputation:", car['horsepower'].isnull().sum())
print("NaN values in liters after imputation:", car['liters'].isnull().sum())


cat_columns = ['brand', 'fuel_type', 'transmission', 'ext_col', 'int_col', 'accident', 'clean_title', 'model_grouped']
cat_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
car_cat_encoded = pd.DataFrame(cat_encoder.fit_transform(car[cat_columns]),
                               columns=cat_encoder.get_feature_names_out(cat_columns),
                               index=car.index)
car = car.drop(cat_columns, axis=1)
car = pd.concat([car, car_cat_encoded], axis=1)

plt.figure(figsize=(10, 6))
plt.hist(car['log_milage'], bins=50)
plt.title('Distribution of Log(Milage) After Capping')
plt.xlabel('Log(Milage)')
plt.ylabel('Frequency')
# Insight: Capping has removed extreme values, centering the distribution around 0 to 1.5.
plt.show()


# Log-transform and cap the target (price)
car_labels_log = np.log1p(car_labels)
lower = car_labels_log.quantile(0.05)
upper = car_labels_log.quantile(0.95)
car_labels_log = car_labels_log.clip(lower, upper)

plt.figure(figsize=(10, 6))
plt.hist(car_labels_log, bins=50)
plt.title('Distribution of Log(Price) After Capping')
plt.xlabel('Log(Price)')
plt.ylabel('Frequency')
# Insight: Capping has reduced outliers, with the distribution peaking around 10.5 to 11.
plt.show()

#
num_columns = ['car_age', 'log_milage', 'horsepower', 'liters']
scaler = StandardScaler()
car[num_columns] = scaler.fit_transform(car[num_columns])

# Final check for NaN values in the entire dataset
print("NaN values in the dataset before splitting:")
print(car.isnull().sum().sum())

X_train, X_test, y_train, y_test = train_test_split(car, car_labels_log, test_size=0.2, random_state=42)
print("Training set shape:", X_train.shape, "Test set shape:", X_test.shape)

lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

y_pred_lin = lin_reg.predict(X_test)
y_test_exp = np.expm1(y_test)

y_pred_lin_exp = np.expm1(y_pred_lin)
lin_rmse = root_mean_squared_error(y_test_exp, y_pred_lin_exp)
print("Linear Regression RMSE on test set (original price scale):", lin_rmse)

lin_rmses = -cross_val_score(lin_reg, X_train, y_train, scoring=rmse_scorer, cv=5)
print("Linear Regression Cross-Validated RMSE (original price scale):", -np.mean(lin_rmses))
pd.Series(lin_rmses).describe()