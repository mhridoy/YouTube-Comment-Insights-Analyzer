document.getElementById('analyzeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const videoUrl = document.getElementById('videoUrl').value;
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');

    loadingDiv.style.display = 'block';
    errorDiv.style.display = 'none';
    resultsDiv.style.display = 'none';

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `video_url=${encodeURIComponent(videoUrl)}`
    })
    .then(response => response.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        if (data.error) {
            errorDiv.textContent = data.error;
            errorDiv.style.display = 'block';
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        errorDiv.textContent = 'An error occurred while analyzing the comments.';
        errorDiv.style.display = 'block';
        console.error('Error:', error);
    });
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';

    document.getElementById('summary').innerHTML = `<h3>Summary</h3><p>${data.summary}</p>`;
    document.getElementById('classification').innerHTML = `<h3>Classification</h3>${data.classification}`;
    document.getElementById('topTopics').innerHTML = `<h3>Top Topics</h3>${data.top_topics}`;
    document.getElementById('keyPhrases').innerHTML = `<h3>Key Phrases</h3>${data.key_phrases}`;

    if (data.ai_image_url) {
        document.getElementById('aiImage').innerHTML = `<h3>AI Generated Image</h3><img src="${data.ai_image_url}" alt="AI Generated Image">`;
    }

    // Create visualizations
    if (data.visualization_data) {
        createChart('sentimentChart', JSON.parse(data.visualization_data.sentiment_chart));
        createChart('topicsChart', JSON.parse(data.visualization_data.topics_chart));
        createChart('emotionChart', JSON.parse(data.visualization_data.emotion_chart));
    }
}

function createChart(elementId, chartData) {
    Plotly.newPlot(elementId, chartData.data, chartData.layout);
}
