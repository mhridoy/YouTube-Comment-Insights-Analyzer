import os
import json
import logging
import traceback
from flask import Flask, render_template, request, jsonify
from youtube_api import get_video_comments, get_video_id
from comment_analysis import analyze_comments_with_model
from openai_api import generate_ai_image

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form.get('video_url', '').strip()
    if not video_url:
        return jsonify({'error': 'No YouTube URL provided.'}), 400

    try:
        video_id = get_video_id(video_url)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL.'}), 400

        # Fetch comments (with caching)
        comments = get_video_comments(video_url, max_results=500)
        if not comments:
            return jsonify({'error': 'No comments fetched. Please ensure the video has comments enabled.'}), 400

        # Analyze comments
        analysis = analyze_comments_with_model(comments)
        if not analysis:
            return jsonify({'error': 'Failed to analyze comments.'}), 500

        # Generate AI image based on summary
        ai_image_url = generate_ai_image(analysis.get('summary', ''))
        analysis['ai_image_url'] = ai_image_url or ''

        # Include visualization data in the response
        visualization_data = {
            'sentiment_chart': analysis.get('sentiment_chart', '{}'),
            'topics_chart': analysis.get('topics_chart', '{}'),
            'emotion_chart': analysis.get('emotion_chart', '{}')
        }
        analysis['visualization_data'] = visualization_data

        logger.info(f"Analysis completed for video ID: {video_id}")

        return jsonify(analysis)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logger.error(error_message)
        logger.error(traceback.format_exc())
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    # Ensure environment variables are set
    required_env_vars = ['OPENAI_API_KEY', 'YOUTUBE_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        exit(1)

    app.run(host='0.0.0.0', port=5000, debug=True)
