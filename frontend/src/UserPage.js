import React, { useState } from 'react';
import axios from 'axios';

function UserPage() {
    const [predictions, setPredictions] = useState([]);
    const [error, setError] = useState('');

    const fetchPredictions = async () => {
        try {
            setError('');
            const response = await axios.get('http://localhost:5000/api/predictions');
            setPredictions(response.data);
        } catch (err) {
            setError('Failed to fetch predictions.');
            console.error(err);
        }
    };

    return (
        <div>
            <h1>User Predictions</h1>
            <button onClick={fetchPredictions}>View Predictions</button>
            {error && <div className="error">{error}</div>}
            <div className="predictions">
                {predictions.map((pred, index) => (
                    <div key={index} className="prediction">
                        <h3>Story #{index + 1}</h3>
                        <p><strong>Budget:</strong> {pred.budget_prediction}</p>
                        <p><strong>Timeline:</strong> {pred.timeline_prediction}</p>
                        <p><strong>Team Skills:</strong> {pred.team_skills_prediction.join(', ')}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default UserPage;
