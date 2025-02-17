import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminPage() {
    const [changeRequests, setChangeRequests] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchChangeRequests = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/change-requests');
                setChangeRequests(response.data);
            } catch (err) {
                console.error('Error fetching change requests:', err);
                setError('Failed to fetch change requests.');
            }
        };

        fetchChangeRequests();
    }, []);

    return (
        <div>
            <h2>Admin - View Change Requests</h2>
            {error && <div className="error">{error}</div>}
            {changeRequests.map((request, index) => (
                <div key={index}>
                    <p><strong>Project ID:</strong> {request.projectId}</p>
                    <p><strong>Story ID:</strong> {request.storyId}</p>
                    <p><strong>Message:</strong> {request.message}</p>
                    <p><strong>Created At:</strong> {new Date(request.createdAt).toLocaleString()}</p>
                    <hr />
                </div>
            ))}
        </div>
    );
}

export default AdminPage;
