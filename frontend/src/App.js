import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StoryPredictionPage from './StoryPredictionPage';
import ViewProjectPage from './ViewProjectPage';
import AdminPage from './AdminPage';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <h1>User Story Dashboard</h1>
                <nav>
                    <ul>
                        <li><Link to="/">Predict Stories</Link></li>
                        <li><Link to="/view-project">View Project</Link></li>
                        <li><Link to="/admin">Admin</Link></li>
                    </ul>
                </nav>
                <Routes>
                    <Route path="/" element={<StoryPredictionPage />} />
                    <Route path="/view-project" element={<ViewProjectPage />} />
                    <Route path="/admin" element={<AdminPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
