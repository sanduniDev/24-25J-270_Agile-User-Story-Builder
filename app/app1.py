from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load model and preprocessing objects
rf_model = joblib.load('../models/final_priority_model.pkl')
label_encoders = joblib.load('../models/label_encoders.pkl')
scaler = joblib.load('../models/scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from POST request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Convert input to DataFrame
        new_data = pd.DataFrame([data])

        # Define correct feature order (must match training data)
        model_feature_order = ['stakeholder_role', 'complexity', 'moscow_category', 'weighted_score', 'project_stage', 'outcome']

        # Validate feature presence and reorder
        missing_features = [feature for feature in model_feature_order if feature not in new_data.columns]
        if missing_features:
            return jsonify({'error': 'Missing required features', 'missing_features': missing_features}), 400
        new_data = new_data[model_feature_order]

        # Convert numerical fields to numeric types
        numerical_features = ['complexity', 'weighted_score']
        for feature in numerical_features:
            new_data[feature] = pd.to_numeric(new_data[feature], errors='coerce')

        # Check for non-numeric values
        if new_data[numerical_features].isnull().any().any():
            return jsonify({'error': 'Non-numeric values detected in numerical fields', 'numerical_fields': numerical_features}), 400

        # Encode categorical fields
        for col, le in label_encoders.items():
            if col in new_data.columns:
                new_data[col] = new_data[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        # Scale numerical features
        new_data[numerical_features] = scaler.transform(new_data[numerical_features])

        # Predict
        prediction = rf_model.predict(new_data)
        priority_mapping = {0: 'Low', 1: 'Medium', 2: 'High'}
        return jsonify({'predicted_priority': priority_mapping[prediction[0]]})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
