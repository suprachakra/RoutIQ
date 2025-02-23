## 2. Demand Forecasting Model (demand_model.pkl)

### Description
- A serialized model (using pickle) that forecasts future demand based on historical trends and external variables.
- Can be a Gradient Boosting Regressor or an LSTM-based model, depending on data complexity.

### Model Architecture & Process
- **For Gradient Boosting:**  
  - Uses an ensemble of decision trees; hyperparameters include n_estimators, learning_rate, and max_depth.
- **For LSTM (if applicable):**  
  - Uses recurrent layers to capture temporal dependencies in demand data.
- **Training:**  
  - Split historical demand data into training and test sets.
  - Train the model using appropriate libraries (scikit-learn for Gradient Boosting, TensorFlow/Keras for LSTM).
  - Evaluate using cross-validation and backtesting to ensure forecast accuracy within target confidence intervals.

### How to Generate & Use
- **Training Script:** 

1. Train a regression model (e.g., Gradient Boosting Regressor or LSTM-based model) on historical demand data.
2. Example training snippet:
```
from sklearn.ensemble import GradientBoostingRegressor
import pickle

demand_model = GradientBoostingRegressor(n_estimators=200)
demand_model.fit(X_train, y_train)
with open("ml/models/demand_model.pkl", "wb") as f:
    pickle.dump(demand_model, f)

```

- **Saving Model:** Use `pickle.dump(model, open("ml/models/demand_model.pkl", "wb"))` after training.

1. Validate using cross-validation and backtesting to ensure forecast accuracy within desired confidence intervals.
2. Regularly update with the latest data for continuous improvement.

- **Inference:** Load the model using `pickle.load(open("ml/models/demand_model.pkl", "rb"))`.

### Evaluation & Maintenance
- Validate forecast accuracy using metrics like MSE and R².
- Schedule periodic retraining to incorporate recent trends.
- Integrate feedback loops to adjust model parameters based on actual performance.
