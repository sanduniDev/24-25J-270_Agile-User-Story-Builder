// const express = require('express');
// const axios = require('axios');
// const cors = require('cors');
// const bodyParser = require('body-parser');

// const app = express();
// const PORT = 5000; 
// const FLASK_API_URL = 'http://127.0.0.1:5000';


// app.use(cors());
// app.use(bodyParser.json());


// app.post('/api/predict', async (req, res) => {
//     try {
//         const response = await axios.post(`${FLASK_API_URL}/predict`, req.body);
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error forwarding predict request:', error.message);
//         res.status(500).json({ error: 'Failed to fetch predictions from Flask API.' });
//     }
// });


// app.post('/api/recompute', async (req, res) => {
//     try {
//         const response = await axios.post(`${FLASK_API_URL}/recompute`, req.body);
//         res.json(response.data);
//     } catch (error) {
//         console.error('Error forwarding recompute request:', error.message);
//         res.status(500).json({ error: 'Failed to process recompute request.' });
//     }
// });

// app.listen(PORT, () => {
//     console.log(`Node.js backend running on http://localhost:${PORT}`);
// });



const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const { v4: uuidv4 } = require('uuid'); // For unique project IDs

const app = express();
const PORT = 5000; // Node.js backend port
const FLASK_API_URL = 'http://127.0.0.1:5000'; // Flask API base URL

// MongoDB connection
const MONGO_URI = 'mongodb://localhost:27017/agile_dashboard';
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch((error) => console.error('MongoDB connection error:', error));

// Define Mongoose schemas and models
const ProjectSchema = new mongoose.Schema({
    projectId: String,
    stories: [
        {
            story_text: String,
            budget_prediction: Number,
            timeline_prediction: Number,
            team_skills_prediction: [String],
        }
    ],
    createdAt: { type: Date, default: Date.now },
});

const ChangeRequestSchema = new mongoose.Schema({
    projectId: String,
    storyId: Number,
    message: String,
    createdAt: { type: Date, default: Date.now },
});

const Project = mongoose.model('Project', ProjectSchema);
const ChangeRequest = mongoose.model('ChangeRequest', ChangeRequestSchema);

// Middleware
app.use(cors());
app.use(bodyParser.json());


app.post('/api/recompute', async (req, res) => {
    const { projectId, story_text, updatedFields } = req.body;

    if (!projectId || !story_text || !updatedFields) {
        return res.status(400).json({ error: 'Missing projectId, story_text, or updatedFields' });
    }

    try {
        // Request recomputation from Flask API
        const response = await axios.post(`${FLASK_API_URL}/recompute`, {
            story_text,
            ...updatedFields,
        });

        const updatedPrediction = response.data;

        // Update specific story in MongoDB
        const project = await Project.findOne({ projectId });
        if (project) {
            const story = project.stories.find((s) => s.story_text === story_text);
            if (story) {
                Object.assign(story, updatedPrediction);
                await project.save();
            }
        }

        res.json(updatedPrediction);
    } catch (error) {
        console.error('Error processing recompute request:', error.message);
        res.status(500).json({ error: 'Failed to process recompute request.' });
    }
});

// Route to handle initial predictions
app.post('/api/predict', async (req, res) => {
    const { projectId, story_texts } = req.body;

    if (!projectId || !story_texts) {
        return res.status(400).json({ error: 'Missing projectId or story_texts' });
    }

    try {
        const response = await axios.post(`${FLASK_API_URL}/predict`, { story_texts });

        const predictions = response.data.map((pred, index) => ({
            story_text: story_texts[index],
            budget_prediction: pred.budget_prediction,
            timeline_prediction: pred.timeline_prediction,
            team_skills_prediction: pred.team_skills_prediction,
        }));

        let project = await Project.findOne({ projectId });
        if (!project) {
            project = new Project({ projectId, stories: predictions });
        } else {
            project.stories.push(...predictions);
        }

        await project.save();
        res.json(project.stories);
    } catch (error) {
        console.error('Error fetching predictions from Flask API:', error.message);
        res.status(500).json({ error: 'Failed to fetch predictions from Flask API.' });
    }
});

// Route to submit a change request
app.post('/api/change-request', async (req, res) => {
    const { projectId, storyId, message } = req.body;

    console.log('Incoming Request:', req.body); // Debug log

    if (!projectId || storyId === undefined || !message) {
        return res.status(400).json({ error: 'Missing projectId, storyId, or message' });
    }

    try {
        const changeRequest = new ChangeRequest({ projectId, storyId, message });
        await changeRequest.save();
        res.json({ success: true, message: 'Change request submitted successfully.' });
    } catch (error) {
        console.error('Error submitting change request:', error.message);
        res.status(500).json({ error: 'Failed to submit change request.' });
    }
});

// Route to fetch all change requests
app.get('/api/change-requests', async (req, res) => {
    try {
        const requests = await ChangeRequest.find({});
        res.json(requests);
    } catch (error) {
        console.error('Error fetching change requests:', error.message);
        res.status(500).json({ error: 'Failed to fetch change requests.' });
    }
});

// Route to fetch project data by projectId
app.get('/api/project/:projectId', async (req, res) => {
    const { projectId } = req.params;

    try {
        const project = await Project.findOne({ projectId });
        if (!project) {
            return res.status(404).json({ error: 'Project not found' });
        }
        res.json(project);
    } catch (error) {
        console.error('Error fetching project:', error.message);
        res.status(500).json({ error: 'Failed to fetch project data.' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Node.js backend running on http://localhost:${PORT}`);
});
