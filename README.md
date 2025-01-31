# 24-25J-270_Agile-User-Story-Builder
Final Year Reseach Project
# Agile User Story Builder

Welcome to the Agile User Story Builder project repository. This project aims to convert informal conversations into structured Agile user stories using advanced technologies like NLP, ML, and predictive analytics.

---

## Overview of the System Components

The Agile User Story Builder is designed with four core components, each addressing a specific aspect of the user story creation and prioritization process:



### **Component 2: Task Identification and Categorization**
- Uses the generated textual user stories to identify tasks.
- Implements a custom algorithm to classify tasks and requirements.
- Builds an ML model for categorizing tasks and non-functional requirements.
- Segregates tasks for effective project tracking and management.

This component extracts, identifies, and categorizes tasks and non-functional requirements (NFRs) from user stories, ensuring efficient project tracking and management. It leverages a custom-trained Random Forest Classifier for accurate classification of tasks and subtasks, while TF-IDF vectorization ensures high-precision text feature extraction. Regex-based sentence segmentation enables structured task organization, supported by text preprocessing for cleaning and normalization. The system differentiates between functional and non-functional requirements, segregating tasks for streamlined workflow management. Additionally, it assigns specific roles to each subtask to ensure clear responsibility allocation, facilitating seamless integration with project tracking tools. The process involves text preprocessing to remove noise, feature extraction using TF-IDF, task segmentation through regex-based sentence structuring, and classification via the Random Forest model. Finally, predefined role mappings ensure that tasks are allocated appropriately within project management systems. By leveraging these methodologies, the component enhances task identification, classification, and assignment, optimizing project efficiency and execution.

## System Architecture

The following diagram illustrates the system architecture of the Agile User Story Builder:[Click Here to View](https://drive.google.com/file/d/1c32_GP-WuX-dX_VAARy7qzemaC3o61Ax/view?usp=sharing)





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
2. Install the required dependencies from the `requirements.txt` file.
3. Configure API keys for speech-to-text and cloud services in the `.env` file.
4. Run the application using the command: `python app.py`.

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
