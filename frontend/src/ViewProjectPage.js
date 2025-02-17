import React, { useState } from 'react';
import axios from 'axios';

function ViewProjectPage() {
    const [projectId, setProjectId] = useState('');
    const [projectData, setProjectData] = useState(null);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [selectedStoryId, setSelectedStoryId] = useState(null);

    const fetchProjectData = async () => {
        try {
            setError('');
            const response = await axios.get(`http://localhost:5000/api/project/${projectId}`);
            setProjectData(response.data);
        } catch (err) {
            setError('Failed to fetch project data.');
            console.error(err);
        }
    };

    const handleSubmitRequest = async () => {
        if (!projectId || selectedStoryId === null || message.trim() === '') {
            setError('Please fill out all fields before submitting.');
            return;
        }

        try {
            const payload = {
                projectId,
                storyId: selectedStoryId,
                message,
            };

            console.log('Payload:', payload); // Debug log
            const response = await axios.post('http://localhost:5000/api/change-request', payload);
            alert(response.data.message);
            setMessage('');
            setSelectedStoryId(null);
        } catch (err) {
            console.error('Error submitting change request:', err);
            setError('Failed to submit change request.');
        }
    };

    return (
        <div>
            <h2>View Project</h2>
            {error && <div className="error">{error}</div>}
            <input
                type="text"
                placeholder="Enter Project ID"
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
            />
            <button onClick={fetchProjectData}>View Project</button>

            {projectData && (
                <div className="project-data">
                    <h3>Project ID: {projectData.projectId}</h3>
                    <h4>Stories:</h4>
                    {projectData.stories.map((story, index) => (
                        <div key={index}>
                            <p><strong>Story Text:</strong> {story.story_text}</p>
                            <p><strong>Budget:</strong> {story.budget_prediction}</p>
                            <p><strong>Timeline:</strong> {story.timeline_prediction}</p>
                            <p><strong>Team Skills:</strong> {story.team_skills_prediction.join(', ')}</p>
                            <button onClick={() => setSelectedStoryId(index)}>Request Change</button>
                        </div>
                    ))}

                    {selectedStoryId !== null && (
                        <div>
                            <textarea
                                placeholder="Enter your change request"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            />
                            <button onClick={handleSubmitRequest}>Submit Request</button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ViewProjectPage;
