import joblib
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Leer el dataset
dataset_path = 'services/mobile_signal/data/mobile_signal_dataset.csv'
data = pd.read_csv(dataset_path)
data = data.dropna(subset=['RSSI'])

# Extraer las características (longitud y latitud) y la variable de respuesta (RSSI)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Ajustar el árbol de decisión
regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(X_train, y_train)

# Hacer predicciones en los conjuntos de entrenamiento y prueba y calcular los scores (R^2)
y_train_pred = regressor.predict(X_train)
train_score = r2_score(y_train, y_train_pred)

y_test_pred = regressor.predict(X_test)
test_score = r2_score(y_test, y_test_pred)

print("Score en entrenamiento (R^2):", train_score)
print("Score en prueba (R^2):", test_score)

# Save the model to a file
joblib.dump(regressor, 'services/mobile_signal/data/rssi_model.pkl')

# Load the model from file
model = joblib.load('services/mobile_signal/data/rssi_model.pkl')

# Use the loaded model to make predictions
longitude = -8.515573
latitude = 51.881049
predicted_rssi = model.predict([[longitude, latitude]])
print(predicted_rssi)
# data = data.dropna(subset=['RSSI'])