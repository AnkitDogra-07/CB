# Chatbot for Technology

This repository contains the code and documentation for the project "Chatbot for Technology," a sophisticated conversational agent designed to assist users by providing statistical insights and personalized recommendations related to programming languages and frameworks. This project was developed as part of the Minor Project (CS3270) course at Manipal University Jaipur.

## Table of Contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Scope](#future-scope)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
The "Chatbot for Technology" project aims to leverage natural language processing (NLP) and artificial intelligence (AI) to create a virtual assistant capable of engaging with users, understanding their queries, and providing relevant information and services. The chatbot primarily serves developers by providing insights derived from the Stack Overflow Developer Survey data.

## Objectives
The key objectives of the project include:
- Implementing NLP capabilities to understand user queries.
- Extracting valuable insights from the Stack Overflow Developer Survey data.
- Providing personalized statistics on programming languages, frameworks, and trends.
- Acting as a virtual assistant to help users make informed decisions about their coding journey.

## Technologies Used
The project utilizes the following technologies:
- **Streamlit**: Provides the frontend interface for user interaction.
- **LangChain and Hugging Face**: Backend technologies for NLP and AI capabilities.

### Streamlit Frontend
Streamlit is used to create an intuitive and interactive user interface that bridges the gap between the backend and the users.

### LangChain and Hugging Face Backend
- **Hugging Face**: Offers a selection of pre-trained language models.
- **LangChain**: Enhances the chatbot's NLP capabilities through prompt engineering and other NLP features such as intent classification, question answering, and text summarization.

## Features
- **User-Friendly Interface**: Accessible via a web interface, ensuring a smooth user experience.
- **NLP and Data Analysis**: Utilizes advanced NLP algorithms to understand and respond to user queries.
- **Personalized Statistics**: Provides users with tailored statistics and recommendations based on their preferences and profile.
- **Resource Recommendations**: Suggests relevant tutorials, documentation, articles, and online courses.
- **Code Review and Feedback**: Offers constructive feedback on coding style and efficiency.

## Installation
To set up the project locally, follow these steps:

### Prerequisites
- Install Python 3.8 or higher.
- Install Docker from the [official website](https://www.docker.com/get-started).

### Steps
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/chatbot-for-technology.git
    cd chatbot-for-technology
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Qdrant Docker container**:
    ```sh
    docker pull qdrant/qdrant
    docker run -p 6333:6333 qdrant/qdrant
    ```

5. **Execute the ingest script**:
    ```sh
    python ingest.py
    ```

6. **Run the Streamlit application**:
    ```sh
    streamlit run app.py
    ```

## Usage
Once the setup is complete, open your web browser and navigate to `http://localhost:8501` to interact with the chatbot. Enter your queries in the chat interface and receive insights and recommendations based on the Stack Overflow Developer Survey data.

## Future Scope
Future enhancements for the chatbot include:
- Expanding NLP capabilities to handle more complex queries.
- Integrating more data sources for richer insights.
- Improving the chatbot's ability to provide real-time assistance and more personalized recommendations.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
We extend our gratitude to our internal supervisor, Dr. Neelam Chaplot, for the constant support and guidance throughout the project. We also thank Dr. Neha Chaudhary, Head of the Department of CSE, and all faculty members and staff for their support.