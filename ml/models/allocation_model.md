## Allocation Model (allocation_model.h5)

### Description
- A pre-trained Keras model that learns optimal fleet allocation based on historical data and real-time inputs.
- Uses a multi-layer neural network to predict the best distribution of vehicles and drivers to meet current and forecasted demand.

### Model Architecture
- **Input Layer:** Accepts a vector of features (e.g., current vehicle locations, historical demand, weather, traffic conditions).
- **Hidden Layers:** Two dense layers (e.g., 128 and 64 neurons) with ReLU activation and dropout for regularization.
- **Output Layer:** A single neuron with linear activation predicting the allocation score.

### Training Process
- **Data:** Historical fleet data including vehicle usage, demand patterns, external factors (weather, traffic).
- **Algorithm:** Adam optimizer with Mean Squared Error (MSE) as the loss function.
- **Validation:** Use a holdout test set to compute MSE and R² metrics.
- **Retraining:** Automate retraining every month using new data, with continuous evaluation.

### How to Generate & Use
- **Training Script:** 
1. Train the model using historical fleet and demand data.
2. Use a multi-layer neural network architecture with dense layers, dropout for regularization, and a final linear activation for regression output.
3. Example training snippet

```
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(128, activation='relu', input_shape=(num_features,)),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(1, activation='linear')
])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
model.save("ml/models/allocation_model.h5")
```
- **Saving Model:** Use `model.save("ml/models/allocation_model.h5")` after training.
1. Evaluate model performance using Mean Squared Error (MSE) and R² metrics on a holdout test set.
2. Continuously retrain as new data becomes available.

- **Inference:** Load the model in the platform using `tf.keras.models.load_model("ml/models/allocation_model.h5")`.

### Evaluation & Maintenance
- Monitor model performance continuously.
- Set up alerts if performance metrics fall below acceptable thresholds.
- Periodically update the training data set and retrain the model.
