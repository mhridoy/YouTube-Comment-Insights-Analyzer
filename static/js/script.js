document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const chartsDiv = document.getElementById('charts');
    const aiImageContainer = document.getElementById('ai-image-container');
    const aiImage = document.getElementById('ai-image');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const videoUrl = document.getElementById('video-url').value.trim();
        if (!videoUrl) {
            alert('Please enter a YouTube video URL.');
            return;
        }

        loadingDiv.classList.remove('hidden');
        resultsDiv.innerHTML = '';
        chartsDiv.innerHTML = `
            <div id="sentiment-chart" class="chart-container glass p-4"></div>
            <div id="topics-chart" class="chart-container glass p-4"></div>
            <div id="emotion-chart" class="chart-container glass p-4 md:col-span-2"></div>
        `;
        aiImageContainer.style.display = 'none';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `video_url=${encodeURIComponent(videoUrl)}`,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to analyze comments');
            }

            const data = await response.json();
            displayResults(data);
            renderCharts(data);
        } catch (error) {
            resultsDiv.innerHTML = `<p class="text-red-300 font-bold">Error: ${error.message}</p>`;
            chartsDiv.innerHTML = '';
            aiImageContainer.style.display = 'none';
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });

    function displayResults(data) {
        let resultsHTML = '<h2 class="text-3xl font-bold mb-6 text-center">Analysis Results</h2>';

        for (const [key, value] of Object.entries(data)) {
            if (!['sentiment_chart', 'topics_chart', 'emotion_chart', 'ai_image_url', 'video_url'].includes(key)) {
                const title = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                resultsHTML += `
                    <div class="mb-6 glass p-6 hover:shadow-lg transition-all duration-300">
                        <h3 class="text-2xl font-semibold mb-4">${title}</h3>
                        <div class="text-gray-200 leading-relaxed">${value}</div>
                    </div>
                `;
            }
        }

        resultsDiv.innerHTML = resultsHTML;

        if (data.ai_image_url) {
            aiImage.src = data.ai_image_url;
            aiImageContainer.style.display = 'block';
        } else {
            aiImageContainer.style.display = 'none';
        }

        resultsDiv.style.opacity = 0;
        let opacity = 0;
        const fadeIn = setInterval(() => {
            if (opacity < 1) {
                opacity += 0.1;
                resultsDiv.style.opacity = opacity;
            } else {
                clearInterval(fadeIn);
            }
        }, 50);
    }

    function renderCharts(data) {
        const commonLayout = {
            font: { family: 'Poppins, sans-serif', color: '#ffffff' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            margin: { t: 50, r: 30, l: 30, b: 50 },
        };

        if (data.sentiment_chart) {
            const sentimentChartData = JSON.parse(data.sentiment_chart);
            sentimentChartData.layout = {
                ...sentimentChartData.layout,
                ...commonLayout,
                title: { text: 'Overall Sentiment', font: { size: 24, color: '#ffffff' } },
                hoverlabel: { bgcolor: '#FFF', font: { size: 14 } },
                annotations: sentimentChartData.layout.annotations,
            };

            sentimentChartData.layout.autosize = true;
            sentimentChartData.layout.height = 400;
            sentimentChartData.layout.width = 600;

            Plotly.newPlot('sentiment-chart', sentimentChartData.data, sentimentChartData.layout, { responsive: true });
            document.getElementById('sentiment-chart').classList.add('show');
        }

        if (data.topics_chart) {
            const topicsChartData = JSON.parse(data.topics_chart);
            topicsChartData.layout = {
                ...topicsChartData.layout,
                ...commonLayout,
                title: { text: 'Main Topics Discussed', font: { size: 24, color: '#ffffff' } },
                hoverlabel: { bgcolor: '#FFF', font: { size: 14 } },
                yaxis: { ...topicsChartData.layout.yaxis, tickfont: { size: 14 }, automargin: true },
                margin: { t: 50, r: 30, l: 200, b: 50 },
            };
            Plotly.newPlot('topics-chart', topicsChartData.data, topicsChartData.layout, { responsive: true });
            document.getElementById('topics-chart').classList.add('show');
        }

        if (data.emotion_chart) {
            const emotionChartData = JSON.parse(data.emotion_chart);
            emotionChartData.layout = {
                ...emotionChartData.layout,
                ...commonLayout,
                title: { text: 'Emotional Tone of Comments', font: { size: 24, color: '#ffffff' } },
                hoverlabel: { bgcolor: '#FFF', font: { size: 14 } },
                xaxis: { ...emotionChartData.layout.xaxis, tickfont: { size: 14 } },
            };
            Plotly.newPlot('emotion-chart', emotionChartData.data, emotionChartData.layout, { responsive: true });
            document.getElementById('emotion-chart').classList.add('show');
        }

        chartsDiv.querySelectorAll('.chart-container').forEach((chart, index) => {
            setTimeout(() => {
                chart.classList.add('show');
            }, index * 200);
        });
    }
});