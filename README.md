# 24-25J-270_Agile-User-Story-Builder
Final Year Reseach Project
# Agile User Story Builder

Welcome to the Agile User Story Builder project repository. This project aims to convert informal conversations into structured Agile user stories using advanced technologies like NLP, ML, and predictive analytics.

---

## Overview of the System Components

The Agile User Story Builder is designed with four core components, each addressing a specific aspect of the user story creation and prioritization process:

### **Component 1: Data Capture and Initial Processing**
- Captures real-time software development conversations from stakeholders as audio input in WAV format.
- Utilizes Azure Speech-to-Text for accurate transcription and converts spoken requirements into structured text.
- Applies BERT-based NLP models for high-precision requirement classification, distinguishing between functional and non-functional requirements.
- Employs Retrieval-Augmented Generation (RAG) to enhance contextual understanding by retrieving relevant knowledge from a unified repository.
- Uses the T5 transformer model to generate structured user stories, ensuring clarity and completeness.
- Integrates generative AI-powered visualization to represent user stories intuitively for better stakeholder understanding.

**GitHub Repository:** [Component 1](https://github.com/sanduniDev/24-25J-270_Agile-User-Story-Builder/tree/Sathsarani-H.E.S)

### **Component 2: Task Identification and Categorization**
- Uses the generated textual user stories to identify tasks.
- Implements a custom algorithm to classify tasks and requirements.
- Builds an ML model for categorizing tasks and non-functional requirements.
- Segregates tasks for effective project tracking and management.

  **GitHub Repository:** [Component 2](https://github.com/sanduniDev/24-25J-270_Agile-User-Story-Builder/tree/Jasinge-Y.s)

### **Component 3: Predictive Analytics for Feedback and Project Timeline**
- Develops ML models to predict feedback, timelines, and budgets based on user stories.
- Uses custom algorithms to enhance the accuracy of predictions.
- Visualizes predictions and analytics on a separate dashboard for clients and developers.

  
**GitHub Repository:** [Component 3](https://github.com/sanduniDev/24-25J-270_Agile-User-Story-Builder/tree/Jonekkuhewa-R.R)

### **Component 4: User Story Prioritization**
- Applies the MoSCoW prioritization method (Must, Should, Could, Won't).
- Pre-processes data and uses ML models to rank user stories.
- Allows real-time prioritization updates based on stakeholder inputs.
- Displays the prioritized backlog on an interactive dashboard.

  **GitHub Repository:** [Component 4](https://github.com/sanduniDev/24-25J-270_Agile-User-Story-Builder/tree/Waidyasekara-D.S.H)

---

## System Architecture

The following diagram illustrates the system architecture of the Agile User Story Builder:

![System Architecture](https://github.com/user-attachments/assets/002c6e3a-6617-43dd-b066-23aab6118451)



---

## Key Features
1. **Automated Conversation Capture**: Transforms verbal stakeholder communications into structured text.
2. **Advanced NLP Processing**: Leverages NLP and neural networks for requirement categorization.
3. **Dynamic Prioritization**: Real-time adjustment of user story priorities.
4. **Predictive Analytics**: Models to predict project impacts on time, cost, and scope.
5. **Interactive Dashboard**: Allows developers and stakeholders to monitor progress and refine priorities.

---

## Technologies Used
- **Speech-to-Text APIs**: Amazon Transcribe, Azure Cognitive Services
- **Machine Learning Frameworks**: TensorFlow, PyTorch
- **Natural Language Processing**: Tokenization, Lemmatization, Sentiment Analysis
- **Web Technologies**: React, Flask, Node
- **Visualization Tools**: Plotly, Dash

---

## Installation and Setup
To set up the project locally, follow these steps:
1. Clone the repository.
2. Install the required dependencies from the requirements.txt file.
3. Configure API keys for speech-to-text and cloud services in the .env file.
4. Run the application using the command: python app.py.

---

## Contributing
We welcome contributions! Please fork the repository, create a feature branch, and submit a pull request. Ensure your changes align with the project guidelines.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- Faculty of Computing, SLIIT
- Research Supervisors and Mentors
- Stakeholders who participated in the testing phase 
