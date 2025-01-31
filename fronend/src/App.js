import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    stakeholder_role: "",
    complexity: "",
    moscow_category: "",
    weighted_score: "",
    project_stage: "",
    outcome: "",
  });

  const [userStory, setUserStory] = useState("");
  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  // Logic to process user story and populate fields
  const processUserStory = () => {
    if (!userStory) {
      setError("Please enter a user story.");
      return;
    }

    // Example logic: map user stories to form fields based on keywords
    let stakeholder_role = "";
    let complexity = 10;
    let moscow_category = 3; // Default "Won't have"
    let weighted_score = 5;
    let project_stage = 0; // Default "Planning"
    let outcome = 0; // Default "Approved"



// Logic for MoSCoW categorization
if (
  userStory.toLowerCase().includes("must") || 
  userStory.toLowerCase().includes("critical") || 
  userStory.toLowerCase().includes("essential")
) {
  moscow_category = 1; // Must Have
} else if (
  userStory.toLowerCase().includes("should") || 
  userStory.toLowerCase().includes("important") || 
  userStory.toLowerCase().includes("needed")
) {
  moscow_category = 2; // Should Have
} else if (
  userStory.toLowerCase().includes("could") || 
  userStory.toLowerCase().includes("optional") || 
  userStory.toLowerCase().includes("nice to have")
) {
  moscow_category = 0; // Could Have
} else {
  moscow_category = 3; // Won't Have (default case)
}


  

  // Initialize MoSCoW category

    if (userStory.toLowerCase().includes("customer")) {
      stakeholder_role = 0; // Customer
      complexity = 20;
      weighted_score = 10;
    } else if (userStory.toLowerCase().includes("developer")) {
      stakeholder_role = 1; // Developer
      complexity = 15;
      weighted_score = 8;
    } else if (userStory.toLowerCase().includes("manager")) {
      stakeholder_role = 2; // Manager
      complexity = 10;
      weighted_score = 7;
    } else {
      stakeholder_role = 4; // Default to "Teacher" if no match
    }

    setFormData({
      stakeholder_role,
      complexity,
      moscow_category,
      weighted_score,
      project_stage,
      outcome,
    });
    setError(""); // Clear errors
  };

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "stakeholder_role" ||
        name === "moscow_category" ||
        name === "project_stage" ||
        name === "outcome"
        ? Number(value) // Convert dropdown values to numbers
        : value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors
    setPrediction(""); // Clear previous predictions

    console.log("Form Data Submitted:", formData); // Debug log

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData);
      console.log("Prediction Response:", response.data); // Debug log
      setPrediction(response.data.predicted_priority);
    } catch (err) {
      console.error("Error Response:", err.response?.data || err.message); // Debug log
      setError(err.response?.data?.error || "An error occurred while fetching the prediction.");
    }
  };

  return (
    <div className="container">
      <h1>Priority Prediction</h1>

      {/* Manual User Story Input */}
      <div>
        <label>Enter User Story: </label>
        <textarea
          value={userStory}
          onChange={(e) => setUserStory(e.target.value)}
          placeholder="Type your user story here..."
          rows="4"
          style={{ width: "100%" }}
        />
        <button
          onClick={processUserStory}
          style={{ marginTop: "10px", padding: "10px", backgroundColor: "#007bff", color: "#fff", border: "none", borderRadius: "4px" }}
        >
          Process User Story
        </button>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} style={{ marginTop: "20px" }}>
        <div>
          <label>Stakeholder Role: </label>
          <select
            name="stakeholder_role"
            value={formData.stakeholder_role}
            onChange={handleChange}
            required
          >
            <option value="">Select Stakeholder Role</option>
            <option value="0">Customer</option>
            <option value="1">Developer</option>
            <option value="2">Manager</option>
            <option value="3">Student</option>
            <option value="4">Teacher</option>
          </select>
        </div>
        <div>
          <label>Complexity: </label>
          <input
            type="number"
            name="complexity"
            value={formData.complexity}
            onChange={handleChange}
            placeholder="Enter Complexity"
            required
          />
        </div>
        <div>
          <label>MoSCoW Category: </label>
          <select
            name="moscow_category"
            value={formData.moscow_category}
            onChange={handleChange}
            required
          >
            <option value="">Select MoSCoW Category</option>
            <option value="0">Could Have</option>
            <option value="1">Must Have</option>
            <option value="2">Should Have</option>
            <option value="3">Won’t Have</option>
          </select>
        </div>
        <div>
          <label>Weighted Score: </label>
          <input
            type="number"
            name="weighted_score"
            value={formData.weighted_score}
            onChange={handleChange}
            placeholder="Enter Weighted Score"
            required
          />
        </div>
        <div>
          <label>Project Stage: </label>
          <select
            name="project_stage"
            value={formData.project_stage}
            onChange={handleChange}
            required
          >
            <option value="">Select Project Stage</option>
            <option value="0">Planning</option>
            <option value="1">Development</option>
            <option value="2">Testing</option>
          </select>
        </div>
        <div>
          <label>Outcome: </label>
          <select
            name="outcome"
            value={formData.outcome}
            onChange={handleChange}
            required
          >
            <option value="">Select Outcome</option>
            <option value="0">Approved</option>
            <option value="1">Deferred</option>
          </select>
        </div>
        <button type="submit" style={{ marginTop: "10px" }}>Predict</button>
      </form>

      {prediction && <div className="prediction">{prediction}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App;
