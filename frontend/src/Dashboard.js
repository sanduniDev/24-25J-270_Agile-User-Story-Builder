import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
    return (
        <div className="dashboard">
            <h1>Welcome to the User Story Prediction System</h1>
            <div className="buttons">
                <Link to="/user">
                    <button>User</button>
                </Link>
                <Link to="/admin">
                    <button>Admin</button>
                </Link>
            </div>
        </div>
    );
}

export default Dashboard;
