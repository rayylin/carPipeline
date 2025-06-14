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
from xgboost import XGBRegressor
# import matplotlib.pyplot as plt
from scipy.stats import randint
# import seaborn as sns
import pandas as pd
import numpy as np

from config import usedcar

car = pd.read_csv(usedcar)

print(car.info())
print(car.shape) 

print(car.head())

print(car.isnull().sum())
print(car.describe())

# Clean 'price' and 'milage' columns
car['price'] = car['price'].str.replace('$', '').str.replace(',', '').astype(int) # $9,000 -> 9000 
car['milage'] = car['milage'].str.replace(' mi.', '').str.replace(',', '').astype(int)

# Custom RMSE function
def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Custom scorer for original scale
def rmse_original(y_true, y_pred):
    y_true_exp = np.expm1(y_true)
    y_pred_exp = np.expm1(y_pred)
    return np.sqrt(mean_squared_error(y_true_exp, y_pred_exp))

rmse_scorer = make_scorer(rmse_original, greater_is_better=False)

model_counts = car['model'].value_counts()
car['model_grouped'] = car['model'].apply(lambda x: x if model_counts[x] >= 10 else 'Other')

top_models = car['model_grouped'].value_counts().head(10)
car['brand'].value_counts().head(10)
car['fuel_type'].value_counts(dropna=False)




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


# Feature Engineering -- Extract horsepower and liters with improved imputation
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

# Car age
car['car_age'] = 2025 - car['model_year']
# Log transform milage
car['log_milage'] = np.log(car['milage'] + 1)

car = car.drop(['model_year', 'model', 'engine', 'milage'], axis=1)

# Encode Categorical Features
cat_columns = ['brand', 'fuel_type', 'transmission', 'ext_col', 'int_col', 'accident', 'clean_title', 'model_grouped']
cat_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
car_cat_encoded = pd.DataFrame(cat_encoder.fit_transform(car[cat_columns]),
                               columns=cat_encoder.get_feature_names_out(cat_columns),
                               index=car.index)
car = car.drop(cat_columns, axis=1)
car = pd.concat([car, car_cat_encoded], axis=1)

# plt.figure(figsize=(10, 6))
# plt.hist(car['log_milage'], bins=50)
# plt.title('Distribution of Log(Milage) After Capping')
# plt.xlabel('Log(Milage)')
# plt.ylabel('Frequency')
# # Insight: Capping has removed extreme values, centering the distribution around 0 to 1.5.
# plt.show()


# Log-transform and cap the target (price)
car_labels_log = np.log1p(car_labels)
lower = car_labels_log.quantile(0.05)
upper = car_labels_log.quantile(0.95)
car_labels_log = car_labels_log.clip(lower, upper)

# plt.figure(figsize=(10, 6))
# plt.hist(car_labels_log, bins=50)
# plt.title('Distribution of Log(Price) After Capping')
# plt.xlabel('Log(Price)')
# plt.ylabel('Frequency')
# # Insight: Capping has reduced outliers, with the distribution peaking around 10.5 to 11.
# plt.show()

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



# Random Forest
param_dist_rf = {'n_estimators': randint(100, 500), 'max_depth': [None, 10, 20, 30], 'min_samples_split': randint(2, 10)}
rf_random = RandomizedSearchCV(RandomForestRegressor(random_state=42), param_dist_rf, n_iter=10, cv=5, scoring=rmse_scorer, random_state=42)
rf_random.fit(X_train, y_train)

best_rf_model = rf_random.best_estimator_
y_pred_best_rf = best_rf_model.predict(X_test)
y_pred_best_rf_exp = np.expm1(y_pred_best_rf)
rf_rmse = root_mean_squared_error(y_test_exp, y_pred_best_rf_exp)
print("Tuned Random Forest RMSE on test set (original price scale):", rf_rmse)

rf_rmses = -cross_val_score(best_rf_model, X_train, y_train, scoring=rmse_scorer, cv=5)
print("Tuned Random Forest Cross-Validated RMSE (original price scale):", -np.mean(rf_rmses))
pd.Series(rf_rmses).describe()


# XGBoost
param_dist_xgb = {'n_estimators': randint(100, 500), 'max_depth': [3, 6, 9], 'learning_rate': [0.001, 0.01, 0.1, 0.3, 0.5]}
xgb_random = RandomizedSearchCV(XGBRegressor(random_state=42), param_dist_xgb, n_iter=10, cv=5, scoring=rmse_scorer, random_state=42)
xgb_random.fit(X_train, y_train)

xgb_model = xgb_random.best_estimator_
y_pred_xgb = xgb_model.predict(X_test)
y_pred_xgb_exp = np.expm1(y_pred_xgb)
xgb_rmse = root_mean_squared_error(y_test_exp, y_pred_xgb_exp)
print("XGBoost RMSE on test set (original price scale):", xgb_rmse)

xgb_rmses = -cross_val_score(xgb_model, X_train, y_train, scoring=rmse_scorer, cv=5)
print("XGBoost Cross-Validated RMSE (original price scale):", -np.mean(xgb_rmses))
pd.Series(xgb_rmses).describe()



summary = pd.DataFrame({
    'Model': ['Linear Regression', 'Tuned Random Forest', 'XGBoost'],
    'Test RMSE': [lin_rmse, rf_rmse, xgb_rmse],
    'CV RMSE': [-np.mean(lin_rmses), -np.mean(rf_rmses), -np.mean(xgb_rmses)]
})
print(summary)












# Plot for Linear Regression
# plt.figure(figsize=(10, 6))
# plt.scatter(y_test_exp, y_pred_lin_exp, alpha=0.5)
# plt.plot([y_test_exp.min(), y_test_exp.max()], [y_test_exp.min(), y_test_exp.max()], 'r--', lw=2)
# plt.xlabel('Actual Price')
# plt.ylabel('Predicted Price')
# plt.title('Actual vs. Predicted Prices (Linear Regression)')
# plt.show()
# Insight: The plot shows that the Linear Regression model underestimates high actual prices and has significant prediction errors,indicating
# it may not capture complex patterns in the data well.