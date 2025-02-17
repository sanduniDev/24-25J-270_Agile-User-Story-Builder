import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [stories, setStories] = useState(['']); // User story inputs
    const [predictions, setPredictions] = useState([]); // Predictions from the backend
    const [error, setError] = useState(''); // Error message

    // Add a new user story
    const handleAddStory = () => setStories([...stories, '']);

    // Remove a user story
    const handleRemoveStory = (index) => setStories(stories.filter((_, i) => i !== index));

    // Update a user story input
    const handleStoryChange = (index, value) =>
        setStories(stories.map((story, i) => (i === index ? value : story)));

    // Fetch initial predictions
    const handleSubmit = async () => {
        try {
            setError('');
            const response = await axios.post('http://localhost:5000/api/predict', {
                story_texts: stories,
            });
            setPredictions(response.data);
        } catch (err) {
            setError('Failed to fetch predictions.');
            console.error(err);
        }
    };

    // Recompute predictions
    const handleRecompute = async (index, updatedFields) => {
        try {
            setError('');
    
            const storyToRecompute = {
                story_text: predictions[index].story_text, // Original story text
                ...updatedFields, // Add updated fields (budget, timeline, team skills)
            };
    
            console.log('Recompute Payload:', storyToRecompute); // Debug the payload
    
            const response = await axios.post('http://localhost:5000/api/recompute', storyToRecompute);
    
            // Update the specific prediction in the list
            setPredictions((prev) =>
                prev.map((pred, i) => (i === index ? response.data : pred))
            );
        } catch (err) {
            setError('Failed to recompute predictions.');
            console.error('Error in recompute:', err);
        }
    };
    

    return (
        <div className="App">
            <h1>User Story Prediction</h1>
            {error && <div className="error">{error}</div>}
            <div className="story-container">
                {stories.map((story, index) => (
                    <div key={index} className="story-input">
                        <textarea
                            value={story}
                            onChange={(e) => handleStoryChange(index, e.target.value)}
                            placeholder={`Enter user story #${index + 1}`}
                        />
                        <button onClick={() => handleRemoveStory(index)}>Remove</button>
                    </div>
                ))}
                <button onClick={handleAddStory}>Add Story</button>
                <button onClick={handleSubmit}>Get Predictions</button>
            </div>

            {predictions.length > 0 && (
                <div className="predictions">
                    <h2>Predictions</h2>
                    {predictions.map((pred, index) => (
                        <div key={index} className="prediction">
                            <h3>Story #{index + 1}</h3>
                            <p><strong>Budget:</strong> {pred.budget_prediction}</p>
                            <input
                                type="number"
                                placeholder="Update Budget"
                                onBlur={(e) =>
                                    handleRecompute(index, {
                                        budget_prediction: parseFloat(e.target.value),
                                    })
                                }
                            />
                            <p><strong>Timeline:</strong> {pred.timeline_prediction}</p>
                            <input
                                type="number"
                                placeholder="Update Timeline"
                                onBlur={(e) =>
                                    handleRecompute(index, {
                                        timeline_prediction: parseFloat(e.target.value),
                                    })
                                }
                            />
                            <p><strong>Team Skills:</strong> {pred.team_skills_prediction.join(', ')}</p>
                            <input
                                type="text"
                                placeholder="Update Team Skills (comma-separated)"
                                onBlur={(e) =>
                                    handleRecompute(index, {
                                        team_skills_prediction: e.target.value.split(','),
                                    })
                                }
                            />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default App;
