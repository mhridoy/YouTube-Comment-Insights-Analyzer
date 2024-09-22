

# YouTube Comment Insights Analyzer

The **YouTube Comment Insights Analyzer** is a tool designed to extract, analyze, and visualize insights from YouTube video comments. It leverages machine learning and AI techniques to provide valuable feedback about the sentiment, emotion, and topics discussed in YouTube video comments. The tool can also generate AI-powered images to represent visual insights based on the comments.

# Live Demo
[Live Site Link](https://demo.binarybeat.org)

## Features

- **Sentiment Analysis**: Analyze the overall sentiment of the comments (positive, negative, or neutral).
- **Topic Modeling**: Identify key topics discussed in the comments.
- **Emotion Detection**: Detect the emotions conveyed in the comments.
- **AI-Generated Images**: Generate visual representations based on the analysis results.
- **Visualization**: Provides interactive charts for sentiment distribution, topic modeling, and emotional tone.

## How It Works

1. **Input**: The user provides a YouTube video URL.
2. **Comment Extraction**: The system uses YouTube's API to extract comments from the video.
3. **Processing**: The comments are analyzed for sentiment, topics, and emotions using various machine learning techniques, powered by APIs such as OpenAI's API.
4. **Visualization**: The results are displayed using interactive charts (Plotly) and an AI-generated image, giving a comprehensive understanding of the audience's reaction to the video.

### Backend Files:
- **`youtube_api.py`**: This file fetches YouTube comments using the YouTube Data API.
- **`openai_api.py`**: Utilizes the OpenAI API for generating insights, including sentiment, emotion detection, and AI-generated images.
- **`comment_analysis.py`**: Contains the core logic for analyzing the comments using natural language processing (NLP) techniques.
- **`main.py`**: Manages the application workflow, linking the API services with the analysis logic and generating results for visualization.
- **`create_github_repo.py`**: Handles automated repository creation and pushes updates to GitHub.

### Frontend:
- **`index.html`**: The main user interface allows users to input the YouTube video URL and displays the results in an intuitive and interactive way, using Plotly.js for charts and TailwindCSS for styling.

## Installation

### Prerequisites

- Python 3.x
- Pip (Python package installer)
- GitHub account and personal access token
- A YouTube Data API Key
- OpenAI API Key

### Steps to Set Up the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mhridoy/YouTube-Comment-Insights-Analyzer.git
   cd YouTube-Comment-Insights-Analyzer
   ```

2. **Install Required Packages**
   Install the necessary Python libraries using the provided `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**
   You'll need to set the environment variables for the API keys:
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export YOUTUBE_API_KEY="your_youtube_api_key"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```
   This will start the backend processing and API setup.

5. **Access the Frontend**
   Open `index.html` in your web browser to interact with the YouTube Comment Analyzer interface. Paste the URL of the YouTube video to begin the analysis.

## Workflow

1. **User Interface**: Users submit a YouTube video URL via the frontend form (`index.html`).
2. **YouTube Comment Extraction**: The backend script (`youtube_api.py`) fetches the comments.
3. **Analysis**:
    - Sentiment and emotion are analyzed via the `openai_api.py`.
    - Topics are extracted and visualized.
4. **Results**: The results, including sentiment charts, topic modeling, and emotion charts, are displayed via the interactive frontend.
5. **GitHub Automation**: The project files are automatically pushed to a GitHub repository using the `create_github_repo.py`.

## Future Scope

- **Multilingual Support**: Extend support to analyze comments in multiple languages.
- **Customizable Analysis**: Allow users to choose specific aspects of analysis, such as sentiment only or topics only.
- **Real-Time Updates**: Enable live tracking of comments for dynamic analysis on live-streamed videos.
- **Advanced Visualizations**: Add more complex visualizations, such as heatmaps or network graphs for topic relationships.
- **User Sentiment Prediction**: Predict possible user behavior based on the sentiment and emotions of their comments.
- **Scalability**: Allow analysis of comments from multiple videos simultaneously or a batch of videos over a specific channel.
