from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3001"])  # Allow CORS requests from React frontend

# Load model and preprocessing objects
rf_model = joblib.load('../models/final_priority_model.pkl')
label_encoders = joblib.load('../models/label_encoders.pkl')
scaler = joblib.load('../models/scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from POST request
    data = request.get_json()

    # Create DataFrame from input
    new_data = pd.DataFrame([data])

    # Ensure correct column order
    required_features = ['stakeholder_role', 'complexity', 'moscow_category', 'weighted_score', 'project_stage', 'outcome']
    new_data = new_data[required_features]

    # Encode categorical fields
    invalid_columns = []
    for col, le in label_encoders.items():
        if col in new_data.columns:
            invalid_values = [x for x in new_data[col] if x not in le.classes_]
            if invalid_values:
                invalid_columns.append({'column': col, 'invalid_values': invalid_values})
            try:
                new_data[col] = new_data[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
            except:
                return jsonify({'error': f"Invalid category in {col}: {new_data[col].values[0]}"})
    
    # Check for invalid categories
    if invalid_columns:
        return jsonify({'error': 'Some categories are invalid.', 'details': invalid_columns})

    # Scale numerical features
    numerical_features = ['weighted_score', 'complexity']
    new_data[numerical_features] = scaler.transform(new_data[numerical_features])

    # Predict
    prediction = rf_model.predict(new_data)
    priority_mapping = {0: 'Low', 1: 'Medium', 2: 'High'}
    human_readable_prediction = priority_mapping[prediction[0]]

    # Return prediction
    return jsonify({'predicted_priority': human_readable_prediction})


if __name__ == '__main__':
    app.run(debug=True)
